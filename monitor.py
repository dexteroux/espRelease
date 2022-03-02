import subprocess
import json
from datetime import datetime
import requests
import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms
import huaweisms.api.device
url = 'https://localhost/client'
lastUpdate = None
val = requests.get('{0}/default/lastUpdated'.format(url), verify=False, timeout=20)
res = val.json()
if (res):
    lastUpdate = res['lastupdated']
    if (lastUpdate):
        updatedAt = datetime.strptime(lastUpdate, '%Y-%m-%d %H:%M:%S')
        diff = datetime.now() - updatedAt
        print("###", diff.total_seconds()/60)
        if diff.total_seconds()/60 > 15: #15:
            ctx = huaweisms.api.user.quick_login("admin", "start1119", modem_host='192.168.8.1')
            print(ctx)
            information = huaweisms.api.device.information(ctx)  #.device.reboot)
            basic_information = huaweisms.api.device.basic_information(ctx)  #.device.reboot)
            print(information)
            print(basic_information)
            huaweisms.api.device.reboot(ctx)  #.device.reboot)
            device_list = huaweisms.api.wlan.get_connected_hosts(ctx)
            returned_value = subprocess.call('systemctl restart web2pyClientSched.service', shell=True)
            print('returned value:', returned_value)
        pass
pass
