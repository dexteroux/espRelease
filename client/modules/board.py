#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import signal
import sys
import json
from enum import IntEnum
import time
from datetime import datetime
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

def synctime():
    print("attempting time syncronisation ...")
    ser = serial.Serial('/dev/ttyS0', 115200)
    getTime = {'cmd': Commands.GetTime}
    ser.write(("'''" + json.dumps(getTime) + "'''").encode('utf-8'))
    boardts = json.loads(ser.readline())['timeStamp']
    ts = time.time()
    print(boardts, ts)
    if (boardts - ts)**2 > 2:
        print("time stamp doesn't match ...")
        print("time sync in progress ...")
        setTime = {'cmd': Commands.SetTime, 'timeStamp': time.time()}
        ser.write(("'''" + json.dumps(setTime) + "'''").encode('utf-8'))
        if json.loads(ser.readline())['status'] == 1:
            print("time sync done.")
    else:
        print("board time is in sync")
    ser.close()
    return 0

def getConfig():
    print("fetching configuration ...")
    getConfig = {'cmd': Commands.GetConfig}
    ser = serial.Serial('/dev/ttyS0', 115200)
    ser.write(("'''" + json.dumps(getConfig) + "'''").encode('utf-8'))
    config = json.loads(ser.readline())
    ser.close()
    return config['config']
    
def setConfig(config):
    print("pushing configuration ...")
    setConfig = {'cmd': Commands.SetConfig,
				'config': config}
    print(json.dumps(setConfig))
    ser = serial.Serial('/dev/ttyS0', 115200)
    ser.write(("'''" + json.dumps(setConfig) + "'''").encode('utf-8'))
    res = json.loads(ser.readline())
    print(res)
    ser.close()
    return res['status']

    
def readRecord(recordPointer):
    print("fetching Record ...")
    readRecordStr = {'cmd': Commands.ReadRecord, 'recordPointer': recordPointer}
    #print(json.dumps(readRecordStr))
    ser = serial.Serial('/dev/ttyS0', 115200)
    ser.write(("'''" + json.dumps(readRecordStr) + "'''").encode('utf-8'))
    #print(recordPointer, ser.readline())
    res = json.loads(ser.readline())
    ser.close()
    return res['record']


def readRecordAck(startOfRecordPtr):
    acknowledge = {'cmd': Commands.ReadAck, 'startOfRecordPtr': startOfRecordPtr}
    ser = serial.Serial('/dev/ttyS0', 115200)
    ser.write(("'''" + json.dumps(acknowledge) + "'''").encode('utf-8'))
    res = json.loads(ser.readline())
    ser.close()
    return res['status']


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
                "BattVoltage"  : res['BattVoltage'],
                "PMTVoltage"   : res['PMTVoltage'],
                "Pressure"     : res['pressure']
            }
            ddd.append(data)
            #db.rndata.insert(**data)
            #db.commit()
            #board.readRecordAck(i)
        pass
    pass
