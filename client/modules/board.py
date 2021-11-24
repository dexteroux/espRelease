#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import signal
import sys
import json
from enum import IntEnum
import time
from datetime import datetime

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
    readRecord = {'cmd': Commands.ReadRecord, 'recordPointer': recordPointer}
    ser = serial.Serial('/dev/ttyS0', 115200)
    ser.write(("'''" + json.dumps(readRecord) + "'''").encode('utf-8'))
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
    config["serialNo"] = "32323"
    setConfig(config)
    print(readRecord(config['currentRecordPtr']))
    print(readRecordAck(1))
