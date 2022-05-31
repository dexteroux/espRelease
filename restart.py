
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

def handler(signum, frame):
    print("Time out occured ...")
    raise Exception("end of time")

lastUpdate = None
cmd = ['cat', '/proc/uptime']
uptime = float(subprocess.check_output(cmd).decode("utf-8").split(' ')[0])
upTimeInMin = uptime / 60
print(upTimeInMin)
if upTimeInMin > 300:
    print('Rebooting ...')
    board.synctime()
    board.scheduleShutDown()
    os.system("reboot")
else:
    print('Not Rebooting yet ...')

