# -*- coding: utf-8 -*-


from gluon.scheduler import Scheduler
import logging
import board
logger = logging.getLogger("web2py.app.IndraClient")
logger.setLevel(logging.DEBUG)
from gluon import *
from datetime import datetime
import json
import server

def syncConfig():
    config = board.getConfig()
    dbConfig = db().select(db.rn220systems.ALL).first()
    if (config["serialNo"] == dbConfig.SerialNo and
            config["mode"] == dbConfig.devMode and
            config["cycle"] == dbConfig.devCycle):
        config["serialNo"] = dbConfig.SerialNo
        config["mode"] = dbConfig.devMode
        config["cycle"] = dbConfig.devCycle
        board.setConfig(config)
    return 0

def syncBoard():
    execStart = datetime.now()
    board.synctime()
    syncConfig()
    config = board.getConfig()
    currentRecordPtr = config['currentRecordPtr']
    #startOfRecordPtr = config['startOfRecordPtr']
    dbData = db().select(db.rndata.ALL).last()
    if dbData:
        startOfRecordPtr = dbData.Pointer
    else:
        startOfRecordPtr = 0
    ddd = []
    if currentRecordPtr > startOfRecordPtr:
        ddd.append({})
        noOfRecords = currentRecordPtr - startOfRecordPtr
        if (noOfRecords > 100):
            noOfRecords = 100
        for i in range(startOfRecordPtr + 1, startOfRecordPtr + noOfRecords):
            res = board.readRecord(i)
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
            db.rndata.insert(**data)
            db.commit()
            board.readRecordAck(i)
        pass
    execEnd = datetime.now()
    return ('syncBoard', (execEnd - execStart).total_seconds())


def serverSyncConfig():
    execStart = datetime.now()
    server.serverSyncConfiguration(db)
    for i in range(10):
        server.serverSyncRecord(db)
    execEnd = datetime.now()
    return ('serverSyncConfig', (execEnd - execStart).total_seconds())


scheduler = Scheduler(db, tasks=dict(syncBoard=syncBoard, serverSyncConfig=serverSyncConfig))

if not scheduler.task_status(db.scheduler_task.task_name == 'syncBoard', output=True):
    scheduler.queue_task('syncBoard', repeats = 0, retry_failed = -1, period=60)
if not scheduler.task_status(db.scheduler_task.task_name == 'serverSyncConfig', output=True):
    scheduler.queue_task('serverSyncConfig', repeats = 0, retry_failed = -1, period=60, timeout=300)
