import json
from pprint import pprint
from installer import utils

elements = [
    {'file':'/etc/logrotate.d/wvdial',
     'data': '''"/var/log/wvdial.log" {
  copytruncate
  daily
  rotate 1
  compress
  delaycompress
  missingok
  notifempty
}
        ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o644,
    }]



def logrotateSupport(root, info):
    print('... Installing Logrotate Support')
    for element in elements:
        utils.installElem(root, element, info)


