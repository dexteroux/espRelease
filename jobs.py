
import subprocess
import json
import requests
import os
import subprocess
import board
from datetime import date, datetime
import signal
import traceback

url = 'https://localhost/client'
scriptFile = '/home/pi/job.sh'
windows_line_ending = b'\r\n'.decode("utf-8")
linux_line_ending = b'\n'.decode("utf-8")

def runJobs():
    print ("fetching jobs .....")
    try:
        val = requests.get('{0}/default/fetchRemoteJobs'.format(url), verify=False, timeout=20)
        resp = val.json()
        print(resp)
        job = resp['job']
        if job:
            JobScript = job['JobScript']
            JobScript = JobScript.replace(windows_line_ending, linux_line_ending)
            jobFile = open(scriptFile, "w")
            jobFile.write(JobScript)
            jobFile.close()
            subprocess.call(['chmod', '0777', scriptFile])
            result = subprocess.run([scriptFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            job['response'] = result.stdout.decode("utf-8")
            job['error'] = result.stderr.decode("utf-8")
            print("########################")
            val = requests.post('{0}/default/responseRemoteJobs'.format(url), data=json.dumps(job), verify=False, headers={'Content-Type': 'application/json'}, timeout=20)
            #print(val.text)
            resp = val.json()
            print(resp)
    except Exception as e:
        print(traceback.format_exc())
        print("####################")
    return 0

def backup():
    subprocess.call(['rsync', '-azP', '/home/www-data/web2py/applications/client', '/home/pi/backup'])
    return 0


if __name__ == "__main__":
    runJobs()
    backup()
