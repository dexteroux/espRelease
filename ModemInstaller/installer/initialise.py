import subprocess
from pprint import pprint
from installer import utils
import os
from subprocess import call
from pathlib import Path

def initialise():    
    print('... Deleting System Keys')
    for p in Path("/etc/ssh").glob("ssh_host_*"):
        p.unlink()
    #call(['ls', '/etc/ssh'])
    call(['dpkg-reconfigure', 'openssh-server'])
    print('... Setting HostName')
    hostElement = {'file':'/etc/hostname',
                   'data': '''EVPN
     ''',
                   'user': 'root',
                   'group': 'root',
                   'mode': 0o644,
                  }
    response = utils.run(['bash', '-c', "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"])
    serial = response['STDOUT'][:-1]
    print(serial)
    hostElement['data'] = "Host-" + serial.decode()
    utils.installElem('', hostElement, True) 
    utils.replace('/etc/hosts', 'raspberrypi', "Host-" + serial.decode())


