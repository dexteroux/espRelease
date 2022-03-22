import subprocess
import json
import requests
import os
import subprocess
import board
from datetime import date, datetime
import signal
import traceback

def handler(signum, frame):
    print("Time out occured ...")
    raise Exception("end of time")

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

url = 'https://localhost/client'
lastUpdate = None
response = {'actionTaken' : 'None'}
cmd = ['cat', '/proc/uptime']

uptime = float(subprocess.check_output(cmd).decode("utf-8").split(' ')[0])
upTimeInMin = uptime / 60
print(upTimeInMin)
ddd = []
response['upTimeInMin'] = upTimeInMin
try:
    val = requests.get('{0}/default/monitor'.format(url), verify=False, timeout=20)
    dbConfig = val.json()
except Exception as e:
    print(traceback.format_exc())
    print("####################")

if (dbConfig):
    board.synctime()
    config = board.getConfig()
    currentRecordPtr = config['currentRecordPtr']
    try:
        val = requests.get('{0}/default/getRecordPtr'.format(url), verify=False, timeout=20)
        startOfRecordPtr = val.json()['startOfRecordPtr']
        if currentRecordPtr > startOfRecordPtr:
            #ddd.append({})
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
                    "Datetime"     : res['timestamp'], #"2021-10-12T13:27:52",
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
            response['data'] = ddd
        #                                                                                                                                                              db.rndata.insert(**data)
    except Exception as e:
        print(traceback.format_exc())
        print("####################")
        pass
    print(dbConfig)
    BootMode = dbConfig['BootMode']
    PowerOnDuration = dbConfig['PowerOnDuration']
    response['BootMode'] = BootMode
    response['PowerOnDuration'] = 0

    if BootMode == 'PowerSaveMode':
        response['PowerOnDuration'] = PowerOnDuration
        print(PowerOnDuration)
        if upTimeInMin > PowerOnDuration:
            print('Rebooting ...')
            response['actionTaken'] = 'Rebooting'
        else:
            print('Not Rebooting yet ...')
            response['actionTaken'] = 'Not Rebooting'
print(response)

#signal.signal(signal.SIGALRM, handler)
#signal.alarm(40)
try:
    val = requests.post('{0}/default/monitorAck'.format(url), data=json.dumps(dict(response), default=json_serial), verify=False, headers={'Content-Type': 'application/json'}, timeout=20)
    val = requests.get('{0}/default/syncConfig'.format(url), verify=False, timeout=20)
    val = requests.get('{0}/default/syncRecordBunch'.format(url), verify=False, timeout=20)
except Exception as e:
    print(traceback.format_exc())
    print("####################")
    pass
finally:
    #signal.alarm(0)
    pass
print("####################")

if response['actionTaken'] == 'Rebooting':
    board.scheduleShutDown()
    os.system("shutdown -h 5")

'''lastUpdate = res['lastupdated']
    if (lastUpdate):
        updatedAt = datetime.strptime(lastUpdate, '%Y-%m-%d %H:%M:%S')
        diff = datetime.now() - updatedAt
        print(diff.total_seconds()/60)
        if diff.total_seconds()/60 > 15: #15:
        returned_value = subprocess.call('systemctl restart web2pyClientSched.service', shell=True)
        print('returned value:', returned_value)
    pass'''
pass
