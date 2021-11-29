import subprocess
from pprint import pprint
from installer import utils
from subprocess import call


def installPackedges():    
    print('... Installing required system packedges')
    call(['apt-get', 'install', 'nginx', 'python3-virtualenv', 'locate',
          'python3-pip', 'ipsec-tools', 'racoon', 'iptables', 'iptables-persistent',
          'uwsgi', 'vim', 'htop', 'uuid-runtime', 'tcpdump', 'wvdial'])
    call(['pip3', 'install', '-U', 'flask', 'flask_sqlalchemy', 'netifaces', 'flask_wtf', 'requests', 'netaddr', 'uwsgi', 'RPi.GPIO'])
    call(['useradd', '-m', 'www-data'])
    call(['usermod', '-d', '/home/www-data', 'www-data'])
    call(['mkdir', '-p', '/home/www-data'])
    call(['chown', '-R', 'www-data:www-data', '/home/www-data'])


