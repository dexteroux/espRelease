# -*- coding: utf-8 -*-


from gluon.scheduler import Scheduler
import logging
import board
logger = logging.getLogger("web2py.app.IndraClient")
logger.setLevel(logging.DEBUG)
from gluon import *


def syncConfig():
    import board
    import json
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
    execEnd = datetime.now()
    return ('syncBoard', (execEnd - execStart).total_seconds())


scheduler = Scheduler(db, tasks=dict(syncBoard=syncBoard))

if not scheduler.task_status(db.scheduler_task.task_name == 'syncBoard', output=True):
    scheduler.queue_task('syncBoard', repeats = 0, retry_failed = -1, period=300)
