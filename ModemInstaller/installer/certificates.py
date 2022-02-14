import subprocess
import uuid
from pprint import pprint
from installer import utils
from subprocess import call


def generate():    
    print('... Generate Certificates and CSR')
    clientId = "VPNClient-" + str(uuid.uuid4())
    response = utils.run(['bash', '-c', "cat /proc/cpuinfo | grep Serial | cut -d ' ' -f 2"])
    serial = response['STDOUT'][:-1]
    print(serial, clientId)
    #call(['apt-get', 'install', 'nginx', 'python3-virtualenv', 'locate',
    #      'python3-pip', 'ipsec-tools', 'racoon', 'iptables', 'iptables-persistent',
    #      'uwsgi', 'vim', 'htop'])
    #call(['pip3', 'install', 'flask', 'flask_sqlalchemy', 'netifaces', 'flask_wtf', 'requests', 'netaddr', 'uwsgi'])
    #call(['useradd', '-m', 'www-data'])
    #call(['usermod', '-d', '/home/www-data', 'www-data'])
    #call(['mkdir', '-p', '/home/www-data'])
    #call(['chown', '-R', 'www-data:www-data', '/home/www-data'])


