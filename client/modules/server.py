#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

import json
import utils
from datetime import datetime
import requests

def serverSyncConfiguration(db):
    urls = []
    config = {}
    for row in db().select(db.serverConfig.ALL):
        urls.append('{0}/default/syncConfig'.format(row.url))
        localConfig = db().select(db.rn220systems.ALL).first()
        data = []
        del localConfig['update_record']
        del localConfig['delete_record']
        error = ''
        try:
            val = requests.post('{0}/default/syncConfig'.format(row.url), data=json.dumps(dict(localConfig), default=utils.json_serial), verify=False, headers={'Content-Type': 'application/json'})
            remoteConfig = val.json()
            data.append(remoteConfig)
            remoteConfig['UpdatedOn'] = datetime.strptime(remoteConfig['UpdatedOn'], r"%Y-%m-%dT%H:%M:%S")
            remoteConfig['InstallationDate'] = datetime.strptime(remoteConfig['InstallationDate'], r"%Y-%m-%dT%H:%M:%S")
            if (localConfig['UpdatedOn'] >= remoteConfig['UpdatedOn']):
                config = localConfig
            else:
                db(db.rn220systems.SerialNo == remoteConfig['SerialNo']).update(
                    SerialNo         = remoteConfig['SerialNo'],
                    IP               = remoteConfig['IP'],
                    VPNIP            = remoteConfig['VPNIP'],
                    WANIP            = remoteConfig['WANIP'],
                    PORT             = remoteConfig['PORT'],
                    devCycle         = remoteConfig['devCycle'],
                    AutoSet          = remoteConfig['AutoSet'],
                    Status           = remoteConfig['Status'],
                    devLocation      = remoteConfig['devLocation'],
                    Place            = remoteConfig['Place'],
                    devState         = remoteConfig['devState'],
                    TimeOut          = remoteConfig['TimeOut'],
                    CommFail         = remoteConfig['CommFail'],
                    Latitude         = remoteConfig['Latitude'],
                    Longitude        = remoteConfig['Longitude'],
                    Altitude         = remoteConfig['Altitude'],
                    InstallationDate = remoteConfig['InstallationDate'],
                    StationID        = remoteConfig['StationID'],
                    RadonGradient    = remoteConfig['RadonGradient'],
                    RadonExhalation  = remoteConfig['RadonExhalation'],
                    BSNLMobNo        = remoteConfig['BSNLMobNo'],
                    SiteContactNo    = remoteConfig['SiteContactNo'],
                    PersonInCharge   = remoteConfig['PersonInCharge'],
                    SeismicZone      = remoteConfig['SeismicZone'],
                    devMode          = remoteConfig['devMode'],
                    PumpAction       = remoteConfig['PumpAction'],
                    PumpOntime       = remoteConfig['PumpOntime'],
                    PumpOfftime      = remoteConfig['PumpOfftime'],
                    GroupID          = remoteConfig['GroupID'],
                    UpdatedOn        = remoteConfig['UpdatedOn'])
                db.commit()
                config = remoteConfig
        except Exception as ex:
            error = ex
    return dict(localConfig = localConfig, urls=urls, remoteConfig = remoteConfig, config = config, error = str(error), lt = type(localConfig['UpdatedOn']), rt = type(remoteConfig['UpdatedOn']))


def serverSyncRecord(db):
    remotePointers = []
    urls = []
    config = {}
    for row in db().select(db.serverConfig.ALL):
        remotePointer = 0
        recordData = {}
        urls.append('{0}/default/syncConfig'.format(row.url))
        localConfig = db().select(db.rn220systems.ALL).first()
        data = []
        del localConfig['update_record']
        del localConfig['delete_record']
        resp = None
        error = ''
        try:
            val = requests.post('{0}/default/getLastRecordPointer'.format(row.url), data=json.dumps({'SerialNo': localConfig['SerialNo']}, default=utils.json_serial), verify=False, headers={'Content-Type': 'application/json'})
            remotePointer = val.json()
            rrow = db(db.rndata.Pointer > remotePointer).select(orderby=db.rndata.Pointer).first()
            if rrow:
                recordData = dict(rrow)
                recordData.pop('delete_record', None)
                recordData.pop('update_record', None)
                recordData['Datetime'] = datetime.timestamp(recordData['Datetime'])
                resp = requests.post('{0}/default/pushRecord'.format(row.url), json=recordData, verify=False)
        except Exception as ex:
            error = ex
        remotePointers.append({'url': row.url, 'remotePointer': remotePointer, 'recordData': recordData, 'resp': resp}) #remotePointer)
    return dict(remotePointers = remotePointers)
