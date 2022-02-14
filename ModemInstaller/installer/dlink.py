import json
from pprint import pprint
from installer import utils

elements = [
    {'file':'/etc/udev/rules.d/40-dlink.rules',
     'data': '''ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="a407",KERNEL=="sr*", GOTO="switch"
ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="a707",KERNEL=="sr*", GOTO="switch_a707"
ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="a403",KERNEL=="sr*", GOTO="switch_a403"
ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="7d0e",SUBSYSTEM=="usb", GOTO="modprobe"
ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="7d0e",KERNEL=="ttyUSB*", SUBSYSTEM=="tty", GOTO="wvdial"
ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="7d02",SUBSYSTEM=="usb", GOTO="modprobe_7d02"
ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="7d02",KERNEL=="ttyUSB*", SUBSYSTEM=="tty", GOTO="wvdial"
ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="7d0c",SUBSYSTEM=="usb", GOTO="modprobe_7d0c"
ACTION=="add", ATTRS{idVendor}=="2001",ATTRS{idProduct}=="7d0c",KERNEL=="ttyUSB*", SUBSYSTEM=="tty", GOTO="wvdial"
GOTO="end"

LABEL="switch"
ATTRS{bNumInterfaces}==" 1",RUN+="/usr/sbin/usb_modeswitch  -W -c /etc/usb_modeswitch.d/2001_a407"
GOTO="end"

LABEL="switch_a707"
ATTRS{bNumInterfaces}==" 1",RUN+="/usr/sbin/usb_modeswitch  -W -c /etc/usb_modeswitch.d/2001_a707"
GOTO="end"

LABEL="switch_a403"
ATTRS{bNumInterfaces}==" 1",RUN+="/usr/sbin/usb_modeswitch  -W -c /etc/usb_modeswitch.d/2001_a403"
GOTO="end"

LABEL="modprobe"
ATTRS{bNumInterfaces}!=" 1", RUN+="/sbin/modprobe usbserial vendor=0x2001 product=0x7d0e"
GOTO="end"

LABEL="modprobe_7d02"
ATTRS{bNumInterfaces}!=" 1", RUN+="/sbin/modprobe usbserial vendor=0x2001 product=0x7d02"
GOTO="end"

LABEL="modprobe_7d0c"
ATTRS{bNumInterfaces}!=" 1", RUN+="/sbin/modprobe usbserial vendor=0x2001 product=0x7d0c"
GOTO="end"

LABEL="wvdial"
ATTRS{bNumInterfaces}!=" 1", ENV{SYSTEMD_WANTS}="modemdaemon.service"
GOTO="end"

LABEL="end"

        ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o644,
    },
    {'file':'/etc/udev/rules.d/40-huawei.rules',
     'data': '''ACTION=="add", ATTRS{idVendor}=="12d1",ATTRS{idProduct}=="1c20",KERNEL=="sr*", GOTO="switch"
ACTION=="add", ATTRS{idVendor}=="12d1",ATTRS{idProduct}=="14fe", RUN+="usb_modeswitch '/%k'"
ACTION=="add", ATTRS{idVendor}=="12d1",ATTRS{idProduct}=="1506",KERNEL=="ttyUSB*", SUBSYSTEM=="tty", GOTO="wvdial"
ACTION=="add", ATTRS{idVendor}=="12d1",ATTRS{idProduct}=="1f01",KERNEL=="sr*", GOTO="connect"
GOTO="end"

LABEL="switch"
#ATTRS{bNumInterfaces}==" 1",RUN+="/usr/sbin/usb_modeswitch  -W -c /etc/usb_modeswitch.d/12d1_1c20"
ATTRS{bNumInterfaces}==" 1",RUN+="/etc/resetModem.py"
GOTO="end"

LABEL="connect"
RUN+="/usr/sbin/usb_modeswitch -v 0x12d1 -p 0x1f01 -M '55534243123456780000000000000a11062000000000000100000000000000'"
GOTO="end"

LABEL="wvdial"
ATTRS{bNumInterfaces}!=" 1", ENV{SYSTEMD_WANTS}="huawaidaemon.service"
GOTO="end"

LABEL="end"
        ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o644,
    },
    {'file':'/etc/resetModem.py',
     'data': '''#!/usr/bin/python3

# interrupt-based GPIO example using LEDs and pushbuttons

import RPi.GPIO as GPIO
import time
import threading


modemReset = 38
GPIO.setmode(GPIO.BOARD)
GPIO.setup(modemReset, GPIO.OUT)
GPIO.output(modemReset, GPIO.HIGH)

#print("Pin {0} is HIGH".format(modemReset))
time.sleep(10)
GPIO.output(modemReset, GPIO.LOW)


GPIO.cleanup()
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o755,
    },
    {'file':'/etc/systemd/system/modemdaemon.service',
     'data': '''[Unit]
Description=wvdial dialer daemon for 3g dlink usb modem
After=remote-fs.target
After=syslog.target

[Service]
ExecStart=/etc/wvdial.sh
Restart=always
RestartSec=10
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o755,
    },
    {'file':'/etc/systemd/system/huawaidaemon.service',
     'data': '''[Unit]
Description=wvdial dialer daemon for 4g huawai usb modem
After=remote-fs.target
After=syslog.target

[Service]
ExecStart=/etc/wvdialhuawai.sh
Restart=always
RestartSec=10
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o755,
    },
    {'file':'/etc/usb_modeswitch.d/12d1_1c20',
     'data': '''# Huawei 
DefaultVendor=  0x12d1
DefaultProduct= 0x1c20
TargetVendor=0x12d1
TargetProduct=0x1f01
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o644,
    },
    {'file':'/etc/usb_modeswitch.d/12d1_14fe',
     'data': '''# Huawei 
DefaultVendor=  0x12d1
DefaultProduct= 0x14fe
TargetVendor=0x12d1
TargetProduct=0x1506
#HuaweiNewMode=1
#NoDriverLoading=1
MessageContent="55534243123456780000000000000011062000000100000000000000000000"
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o644,
    },
    {'file':'/etc/usb_modeswitch.d/2001_a707',
     'data': '''# D-Link DWM-157 C1
DefaultVendor=  0x2001
DefaultProduct= 0xa707
TargetVendor=0x2001
TargetProduct=0x7d02
StandardEject=1
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o644,
    },
    {'file':'/etc/usb_modeswitch.d/2001_a403',
     'data': '''# D-Link DWM-157 C1
DefaultVendor=  0x2001
DefaultProduct= 0xa403
TargetVendor=0x2001
TargetProduct=0x7d0c
StandardEject=1
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o644,
    },
    {'file':'/etc/usb_modeswitch.d/2001_a407',
     'data': '''# D-Link DWM-157 C1
DefaultVendor=  0x2001
DefaultProduct= 0xa407
TargetVendor=0x2001
TargetProduct=0x7d0e
StandardEject=1
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o644,
    },
    {'file':'/etc/ppp/ip-up.d/000gateway',
     'data': '''#!/bin/sh
# ppp.ip-up hook script for resolvconf
# Written by Roy Marples <roy@marples.name> under the BSD-2 license

/sbin/ip route add default via ${PPP_REMOTE} dev ${PPP_IFACE} metric 100
''',
     'user': 'root',
     'group': 'root',
     'mode': 0o755,
    },
    {'file':'/etc/wvdial.sh',
     'data': '''#!/bin/sh
/bin/echo '#########################' >> /var/log/wvdial.log 2>&1
while [ 1 ]
do
/bin/date >> /var/log/wvdial.log 2>&1
/usr/bin/wvdial >> /var/log/wvdial.log 2>&1
done
''',
     'user': 'root',
     'group': 'root',
     'mode': 0o755,
    },
    {'file':'/etc/wvdialhuawai.sh',
     'data': '''#!/bin/sh
/bin/echo '######Huawai###################' >> /var/log/wvdial.log 2>&1
while [ 1 ]
do
/bin/date >> /var/log/wvdial.log 2>&1
/usr/bin/wvdial Huawai >> /var/log/wvdial.log 2>&1
done
''',
     'user': 'root',
     'group': 'root',
     'mode': 0o755,
    },
    {'file':'/etc/wvdial.conf',
     'data': '''[Dialer Defaults]                                                               
Init1 = ATZ                                                                     
#Init2 = AT+CFUN=0                                                              
#Init3 = AT+CFUN=1                                                              
Init2 = ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0                                       
Init3 = AT+CGDCONT=1,"IP","bsnlstatic"                                          
#Init5 = AT+CGDCONT=1,"IP","airtelgprs.com"                                     
Init4 = AT+CFUN=1,0                                                             
#Init5 = ATDT*99#                                                               
Modem Type = Analog Modem                                                       
#Baud = 9600                                                                    
Baud = 460800                                                                   
New PPPD = yes                                                                  
Modem = /dev/ttyUSB0
ISDN = 0            
Phone = *99#        
Username = " "      
Password = " "      
#Password = airtel  
#Username = airtel 
Stupid Mode = 1     
Carrier Check = no
FlowControl=Hardware(CRTSCTS)
#Dial Command = ADT
Auto Reconnect = off

[Dialer Huawai]
Init1 = ATZ
Init2 = ATQ0 V1 E1 S0=0
Init3 = AT+CGDCONT=1,"IP","bsnlstatic"
Modem Type = Analog Modem
Baud = 9600
New PPPD = yes
Modem = /dev/ttyUSB1
ISDN = 0
Phone = *99#
Username = " "
Password = " "
Stupid Mode = 1
Carrier Check = off
FlowControl=Hardware(CRTSCTS)
Auto Reconnect = off
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o640,
    }]



def installSupport(root, info):
    print('... Installing Dlink Support')
    for element in elements:
        utils.installElem(root, element, info)


