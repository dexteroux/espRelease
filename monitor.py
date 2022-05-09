
import subprocess
import json
import requests
import os
import subprocess
import board
from datetime import date, datetime
import signal
import traceback
import jobs

SERIAL_PORT = "/dev/ttyAMA0"

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
ip = os.popen('dig TXT +short o-o.myaddr.l.google.com @ns1.google.com').readlines()#(-1)[0].strip()
print(ip)
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
print(dbConfig)
if (dbConfig):
    board.synctime()
    #exit(0)
    config = board.getConfig()
    currentRecordPtr = config['currentRecordPtr']
    startOfRecordPtr = config['startOfRecordPtr']
    print(config)
    print(currentRecordPtr)
    try:
        val = requests.get('{0}/default/getRecordPtr'.format(url), verify=False, timeout=20)
        startOfRecordPtr1 = val.json()['startOfRecordPtr']+1
        if (startOfRecordPtr1 > startOfRecordPtr):
            startOfRecordPtr = startOfRecordPtr1
        print(currentRecordPtr, startOfRecordPtr)
        if currentRecordPtr >= startOfRecordPtr:
            #ddd.append({})
            noOfRecords = currentRecordPtr - startOfRecordPtr + 1
            print(noOfRecords)
            if (noOfRecords > 100):
                noOfRecords = 100
            for i in range(startOfRecordPtr, startOfRecordPtr + noOfRecords):
                print("#########################", i)
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
                    "LoadCurrent"  : round(((5.25/2) - res['loadCurrent']) * 5.633, 2),
                    "InputVoltage" : res['inputVoltage'],
                    "BattVoltage"  : res['battVoltage'],
                    "RadonVoltage" : res['radonVoltage'],
                    "PMTVoltage"   : res['PMTVoltage'],
                    "Pressure"     : res['pressure']
                    }
                ddd.append(data)
            response['data'] = ddd
    except Exception as e:
        print(traceback.format_exc())
        print("####################")
        pass
    print(dbConfig)
    BootMode = dbConfig['BootMode']
    PowerOnDuration = dbConfig['PowerOnDuration']
    response['BootMode'] = BootMode
    response['PowerOnDuration'] = 0
    print(dbConfig, config)
    board.syncConfig(dbConfig, config)
    #if BootMode == 'PowerSaveMode':
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
    #print("###################################################0")
    #print(val)
    #print(val.json())
    val = requests.get('{0}/default/syncConfig'.format(url), verify=False, timeout=20)
    #print(val.json())
    val = requests.get('{0}/default/syncRecordBunch'.format(url), verify=False, timeout=20)
    #print(val.json())
except Exception as e:
    print(traceback.format_exc())
    print("####################")
    pass
finally:
    #signal.alarm(0)
    pass
#print("####################")

jobs.runJobs()
if response['actionTaken'] == 'Rebooting':
    board.scheduleShutDown()
    os.system("reboot")
    pass

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
