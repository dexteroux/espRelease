import shutil
import json
from pprint import pprint
from installer import dlink, packedge, certificates, initialise, logrotate

data = json.load(open('menifest.json'))
pprint(data)
initialise.initialise()
packedge.installPackedges()
if data['debug']:
    dlink.installSupport('root', True)
else:
    dlink.installSupport('', True)
certificates.generate()
logrotate.logrotateSupport('', True)    

