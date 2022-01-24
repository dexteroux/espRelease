# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
import json
import utils
import server
from datetime import datetime
import requests

@auth.requires_login()
def index():
    #response.flash = T("Hello World")
    config = db().select(db.rn220systems.ALL).first()
    form=SQLFORM(db.rn220systems, config)
    form.vars = db().select(db.rn220systems.ALL).first()
    form.vars.UpdatedOn = request.now
    form.process(detect_record_change=True)
    if form.record_changed:
        pass
        # do something
    elif form.accepted:
        pass
        # do something else
    else:
        pass
        # do nothing
    return dict(form=form, vars=form.vars)

@auth.requires_login()
def data():
    #export_classes = dict(csv=True, json=False, html=False,
    #                      tsv=False, xml=False, csv_with_hidden_cols=False,
    #                      tsv_with_hidden_cols=False)
    grid = SQLFORM.grid(db.rndata, orderby=~db.rndata.Pointer) #, exportclasses=export_classes)
    return dict(grid=grid)

@auth.requires_login()
def resetDevice():
    import board
    config = board.getConfig()
    dbConfig = db().select(db.rn220systems.ALL).first()
    #if (config["serialNo"] == dbConfig.SerialNo and
    #        config["mode"] == dbConfig.devMode and
    #        config["cycle"] == dbConfig.devCycle):
    #    pass
    #else:
    config["serialNo"] = dbConfig.SerialNo
    config["mode"] = dbConfig.devMode
    config["cycle"] = dbConfig.devCycle
    config["currentRecordPtr"] = -1
    config["startOfRecordPtr"] = 0
    board.setConfig(config)
    db.rndata.truncate()
    db.commit()
    redirect(URL('default','index'))
    return dict(config=json.dumps(config))


def testData():
    import board
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
    return dict(config = config, ddd = ddd) #, dbData=json.dumps(dict(dbData), default=utils.json_serial))


def syncConfig():
    return server.serverSyncConfiguration(db)

def syncRecord():
    return server.serverSyncRecord(db)

def syncRecordBunch():
    return server.serverSyncRecordBunch(db)

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
