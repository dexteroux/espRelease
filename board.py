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

SERIAL_PORT = "/dev/ttyS0"
BAUDRATE = 115200 # 9600
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
    InitPartitions = 12
    PartitionsStatus = 13

def resetBoard():
    print("Reseting Board ...")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(esp_boot, GPIO.OUT)
    GPIO.output(esp_boot, 0)
    time.sleep(1)
    GPIO.output(esp_boot, 1)
    time.sleep(10)
    GPIO.cleanup()

def nocmd():
    print("sending nocmd ...")
    noCmd = {'cmd': Commands.NoCmd}
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200115200)
    ser.write(("'''" + json.dumps(noCmd) + "'''").encode('utf-8'))
    jstr = ser.readline()
    print(jstr)
    #config = json.loads(jstr)
    ser.close()
    return jstr

def synctime():
    print("attempting time syncronisation ...")
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200115200)
    res = os.popen('timedatectl status | grep synchronized').readlines()[0]#(-1)[0].strip()
    try:
        getTime = {'cmd': Commands.GetTime}
        ts = time.time()
        ser.write(("'''" + json.dumps(getTime) + "'''").encode('utf-8'))
        dbuff = ser.readline()
        print(dbuff)
        try:
            boardts = json.loads(dbuff)['timeStamp']
            print(boardts, ts)
        except (UnicodeDecodeError,  json.decoder.JSONDecodeError) as e:
            print("#######################Decode ERROR ####################")
            print(traceback.format_exc())
            print(e)
            boardts = ts
            signal.alarm(20)
            time.sleep(10)
        if res != None and "yes" in res:
            print("System time syncronised!")
            if (boardts - ts)**2 > 8:
                print("time stamp doesn't match ", boardts - ts, "Sec ...")
                print("time sync in progress ...")
                setTime = {'cmd': Commands.SetTime, 'timeStamp': time.time()}
                ser.write(("'''" + json.dumps(setTime) + "'''").encode('utf-8'))
                dbuff = ser.readline()
                print(dbuff)
                if json.loads(dbuff)['status'] == 1:
                    print("time sync done.")
            else:
                print("board time is in sync")
        else:
            if (boardts - ts)**2 > 8:
                res = os.popen('date +%s -s @{0}'.format(boardts)).readlines()#[0]#(-1)[0].strip()
                print(res)
                ts = time.time()
                print(ts)
                #date +%s -s @1371729865
    except Exception as e:
        print("####################### Timeout ERROR ####################")
        print(traceback.format_exc())
        print(e)
        resetBoard()
        ser.reset_input_buffer()
        time.sleep(10)
        pass
    finally:
        signal.alarm(0)
        ser.close()
    return 0

def getConfig():
    print("fetching configuration ...")
    getConfig = {'cmd': Commands.GetConfig}
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200115200)
    ser.write(("'''" + json.dumps(getConfig) + "'''").encode('utf-8'))
    jstr = ser.readline()
    print(jstr)
    config = json.loads(jstr)
    ser.close()
    return config['config']

def setConfig(config):
    print("pushing configuration ...")
    setConfig = {'cmd': Commands.SetConfig,
            'config': config}
    print(json.dumps(setConfig))
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200115200)
    ser.write(("'''" + json.dumps(setConfig) + "'''").encode('utf-8'))
    data = ser.readline()
    print(data)
    res = json.loads(data)
    print(res)
    ser.close()
    return res['status']


def formatPartitions():
    print("formating Partitions ...")
    setConfig = {'cmd': Commands.InitPartitions}
    print(json.dumps(setConfig))
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200115200)
    ser.write(("'''" + json.dumps(setConfig) + "'''").encode('utf-8'))
    dbuff = ser.readline()
    print(dbuff)
    res = json.loads(dbuff)
    print(res)
    ser.close()
    return res['status']

def partitionStatus():
    pstatus = {'cmd': Commands.PartitionsStatus}
    print(json.dumps(pstatus))
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200115200)
    ser.write(("'''" + json.dumps(pstatus) + "'''").encode('utf-8'))
    dbuff = ser.readline()
    print(dbuff)
    res = json.loads(dbuff)
    print(res)
    ser.close()
    return res['PartitionsStatus']

def readRecord(recordPointer):
    print("fetching Record ...")
    readRecordStr = {'cmd': Commands.ReadRecord, 'recordPointer': recordPointer}
    #print(json.dumps(readRecordStr))
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200115200)
    ser.write(("'''" + json.dumps(readRecordStr) + "'''").encode('utf-8'))
    jstr = ser.readline()
    #jstr = ser.readline()
    print(jstr)
    res = json.loads(jstr)
    ser.close()
    return res['record']


def readRecordAck(startOfRecordPtr):
    acknowledge = {'cmd': Commands.ReadAck, 'startOfRecordPtr': startOfRecordPtr}
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200115200)
    ser.write(("'''" + json.dumps(acknowledge) + "'''").encode('utf-8'))
    dbuff = ser.readline()
    print(dbuff)
    res = json.loads(dbuff)
    ser.close()
    return res['status']

def scheduleShutDown():
    scheduleShutDown = {'cmd': Commands.ScheduleShutDown}
    ser = serial.Serial(SERIAL_PORT, BAUDRATE)# 115200)
    ser.write(("'''" + json.dumps(scheduleShutDown) + "'''").encode('utf-8'))
    dbuff = ser.readline()
    print(dbuff)
    res = json.loads(dbuff)
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
    print("$$$$$$$$$$$$$$$$$$$$$")
    print(config)
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

