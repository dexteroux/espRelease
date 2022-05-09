#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import signal
import sys
import json
from enum import IntEnum
import time
from datetime import datetime
import RPi.GPIO as GPIO
import time
import os
import signal
import traceback

SERIAL_PORT = "/dev/ttyAMA0"

esp_en = 17
esp_boot = 27

def handler(signum, frame):
    print("Time out occured ! Need board reset...")
    raise Exception("end of time")

#from sqlalchemy.orm import sessionmaker
#import sqlalchemy as db
#from sqlalchemy.ext.automap import automap_base

localDbUrl = "mysql+mysqlconnector://RnDuo:barc@10.128.1.100:3306/rnduo"

class Commands(IntEnum):
	NoCmd = 0
	SetConfig = 1
	GetConfig = 2
	ReadRecord = 3
	ReadRecords = 4
	ReadAck = 5
	Sleep = 6
	SetTime = 7
	GetTime = 8
	SetCurrentRecordPtr = 9
	GetCurrentRecordPtr = 10
	ScheduleShutDown = 11

def resetBoard():
    print("Reseting Board ...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(esp_boot, GPIO.OUT)
    GPIO.output(esp_boot, 0)
    time.sleep(1)
    GPIO.output(esp_boot, 1)
    time.sleep(10)
    GPIO.cleanup()
    
def synctime():
    print("attempting time syncronisation ...")
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)
    ser = serial.Serial(SERIAL_PORT, 115200)
    res = os.popen('timedatectl status | grep synchronized').readlines()[0]#(-1)[0].strip()
    if res != None and "yes" in res:
        print("System time syncronised!")
        try:
            getTime = {'cmd': Commands.GetTime}
            ser.write(("'''" + json.dumps(getTime) + "'''").encode('utf-8'))
            boardts = json.loads(ser.readline())['timeStamp']
            ts = time.time()
        except Exception as e:
            #print(traceback.format_exc())
            #print(e)
            resetBoard()
            ser.reset_input_buffer()
            getTime = {'cmd': Commands.GetTime}
            ser.write(("'''" + json.dumps(getTime) + "'''").encode('utf-8'))
            boardts = json.loads(ser.readline())['timeStamp']
            ts = time.time()
            pass
        finally:
            signal.alarm(0)
        print(boardts, ts)
        if (boardts - ts)**2 > 8:
            print("time stamp doesn't match ", boardts - ts, "Sec ...")
            print("time sync in progress ...")
            setTime = {'cmd': Commands.SetTime, 'timeStamp': time.time()}
            ser.write(("'''" + json.dumps(setTime) + "'''").encode('utf-8'))
            if json.loads(ser.readline())['status'] == 1:
                print("time sync done.")
        else:
            print("board time is in sync")
    else:
        print("System time not syncronised!")
    ser.close()
    return 0

def getConfig():
    print("fetching configuration ...")
    getConfig = {'cmd': Commands.GetConfig}
    ser = serial.Serial(SERIAL_PORT, 115200)
    ser.write(("'''" + json.dumps(getConfig) + "'''").encode('utf-8'))
    config = json.loads(ser.readline())
    ser.close()
    return config['config']
    
def setConfig(config):
    print("pushing configuration ...")
    setConfig = {'cmd': Commands.SetConfig,
				'config': config}
    print(json.dumps(setConfig))
    ser = serial.Serial(SERIAL_PORT, 115200)
    ser.write(("'''" + json.dumps(setConfig) + "'''").encode('utf-8'))
    res = json.loads(ser.readline())
    print(res)
    ser.close()
    return res['status']

    
def readRecord(recordPointer):
    print("fetching Record ...")
    readRecordStr = {'cmd': Commands.ReadRecord, 'recordPointer': recordPointer}
    #print(json.dumps(readRecordStr))
    ser = serial.Serial(SERIAL_PORT, 115200)
    ser.write(("'''" + json.dumps(readRecordStr) + "'''").encode('utf-8'))
    #print(recordPointer, ser.readline())
    res = json.loads(ser.readline())
    ser.close()
    return res['record']


def readRecordAck(startOfRecordPtr):
    acknowledge = {'cmd': Commands.ReadAck, 'startOfRecordPtr': startOfRecordPtr}
    ser = serial.Serial(SERIAL_PORT, 115200)
    ser.write(("'''" + json.dumps(acknowledge) + "'''").encode('utf-8'))
    res = json.loads(ser.readline())
    ser.close()
    return res['status']

def scheduleShutDown():
    scheduleShutDown = {'cmd': Commands.ScheduleShutDown}
    ser = serial.Serial(SERIAL_PORT, 115200)
    ser.write(("'''" + json.dumps(scheduleShutDown) + "'''").encode('utf-8'))
    res = json.loads(ser.readline())
    ser.close()
    return res['status']

def syncConfig(dbConfig, config):
    #config = getConfig()
    #if (config["serialNo"] == dbConfig.SerialNo and
    #        config["mode"] == dbConfig.devMode and
    #        config["cycle"] == dbConfig.devCycle):
    config["serialNo"] = dbConfig['SerialNo']
    config["mode"]     = dbConfig['devMode']
    config["cycle"]    = dbConfig['devCycle']
    config["ADC0"]     = dbConfig['ADC0']
    config["ADC1"]     = dbConfig['ADC1']
    config["ADC2"]     = dbConfig['ADC2']
    config["ADC3"]     = dbConfig['ADC3']
    config["totalRecords"]     = dbConfig['RecordQueueSize']
    setConfig(config)
    return 0

if __name__ == '__main__':
    synctime()
    config = getConfig()
    print(config)
    currentRecordPtr = config['currentRecordPtr']
    #startOfRecordPtr = config['startOfRecordPtr']
    #dbData = db().select(db.rndata.ALL).last()
    #if dbData:
    #    startOfRecordPtr = dbData.Pointer
    #else:
    startOfRecordPtr = 0
    ddd = []
    if currentRecordPtr > startOfRecordPtr:
        noOfRecords = currentRecordPtr - startOfRecordPtr
        if (noOfRecords > 10):
            noOfRecords = 10
        #print(startOfRecordPtr + 1, startOfRecordPtr + noOfRecords)
        #res = readRecord(3)
        for i in range(startOfRecordPtr + 1, startOfRecordPtr + noOfRecords):
            print(i)
            res = readRecord(i)
            data = {
                "Pointer"      : i,
                "SlNo"         : 0,
                "SerialNo"     : config['serialNo'],
                "devMode"      : config['mode'],
                "devCycle"     : config['cycle'],
                "Datetime"     : datetime.fromtimestamp(res['timestamp']), #"2021-10-12T13:27:52",
                "Counts"       : res['Counts'],
                "BGCounts"     : res['BGCounts'],
                "Concentration": res['Concentration'],
                "Sigma"        : res['Sigma'],
                "Temperature"  : res['temperature'],
                "Humidity"     : res['humidity'],
                "LoadCurrent"  : res['loadCurrent'],
                "InputVoltage" : res['inputVoltage'],
                "BattVoltage"  : res['battVoltage'],
                "RadonVoltage" : res['radonVoltage'],
                "PMTVoltage"   : res['PMTVoltage'],
                "Pressure"     : res['pressure']
            }
            ddd.append(data)
            #db.rndata.insert(**data)
            #db.commit()
            #board.readRecordAck(i)
        pass
    pass

