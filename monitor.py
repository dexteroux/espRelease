import subprocess
import json
from datetime import datetime
import requests
url = 'https://localhost/client'
lastUpdate = None
val = requests.get('{0}/default/lastUpdated'.format(url), verify=False, timeout=20)
res = val.json()
if (res):
	lastUpdate = res['lastupdated']
	if (lastUpdate):
		updatedAt = datetime.strptime(lastUpdate, '%Y-%m-%d %H:%M:%S')
		diff = datetime.now() - updatedAt
		print(diff.total_seconds()/60)
		if diff.total_seconds()/60 > 15: #15:
			returned_value = subprocess.call('systemctl restart web2pyClientSched.service', shell=True)
			print('returned value:', returned_value)
	pass
pass
