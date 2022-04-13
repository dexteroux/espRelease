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
ACTION=="add", ATTRS{idVendor}=="12d1",ATTRS{idProduct}=="1c05",KERNEL=="sr*", GOTO="switch"
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
     /bin/echo     '############### Huawai ######################' >> /var/log/wvdial.log 2>&1
     while [ 1 ]
     do
     /usr/bin/echo "############### DATE ########################" >> /var/log/wvdial.log 2>&1
     /bin/date >> /var/log/wvdial.log 2>&1
     /usr/bin/echo "############### modem-stop #################" >> /var/log/wvdial.log 2>&1
     /usr/bin/wvdial modem-stop >> /var/log/wvdial.log 2>&1
     /usr/bin/sleep 5
     /usr/bin/echo "############### modem-start #################" >> /var/log/wvdial.log 2>&1
     /usr/bin/wvdial modem-start >> /var/log/wvdial.log 2>&1
     /usr/bin/echo "############### set-config #################" >> /var/log/wvdial.log 2>&1
     /usr/bin/wvdial set-new >> /var/log/wvdial.log 2>&1
     /usr/bin/echo "############### info-scan ###################" >> /var/log/wvdial.log 2>&1
     /usr/bin/wvdial info-scan >> /var/log/wvdial.log 2>&1
     /usr/bin/sleep 5
     /usr/bin/echo "############### info-gsm ####################" >> /var/log/wvdial.log 2>&1
     /usr/bin/wvdial info-gsm >> /var/log/wvdial.log 2>&1
     /usr/bin/sleep 10
     /usr/bin/echo "############### info-config #################" >> /var/log/wvdial.log 2>&1
     /usr/bin/wvdial info-config >> /var/log/wvdial.log 2>&1
     /usr/bin/sleep 5
     /usr/bin/echo "############### dialing ####################" >> /var/log/wvdial.log 2>&1
     /usr/bin/wvdial Huawai >> /var/log/wvdial.log 2>&1
     /usr/bin/echo "############### REBOOTING ###################" >> /var/log/wvdial.log 2>&1
     /usr/bin/wvdial modem-reboot >> /var/log/wvdial.log 2>&1
     /usr/bin/sleep 30
     done
''',
     'user': 'root',
     'group': 'root',
     'mode': 0o755,
    },
    {'file':'/etc/wvdial.conf',
     'data': '''[Dialer Defaults]
     Init1 = ATZ
     Init2 = ATQ0 V1 E1 S0=0
     Modem Type = Analog Modem
     ; Phone = <Target Phone Number>
     ISDN = 0
     ; Password = <Your Password>
     ; Username = <Your Login Name>
     Modem = /dev/ttyUSB1
     Baud = 9600
     # If value is set, wvdial will quit after that many tries .If set to 0, wvdial will happily keep
     # dialling forever.
     Dial Attempts = 3

     # The maximum time in seconds that wvdial will wait for a connection to be made. Default value is
     # 60 seconds.
     Dial Timeout = 30

     [Dialer Huawai]
     Init3 = AT+CGDCONT=1,"IP","bsnlstatic"
     Init4 = AT+CGEQMIN=1,4,64,640,64,640
     Init5 = AT+CGEQREQ=1,4,64,640,64,640
     #Init3 = AT+COPS=0
     Phone = *99#
     Username = " "
     Password = " "
     Stupid Mode = 1
     Baud = 9600
     #460800
     FlowControl=Hardware(CRTSCTS)
     Auto Reconnect = off
     Idle Seconds = 0
     Carrier Check = off

     [Dialer modem-start]
     # Set the hardware functionality to a certain level.
     #   AT+CFUN=0: non-cyclic sleep mode, minimal functionality.
     #   AT+CFUN=1: full functionality, no power saving.
     #   AT+CFUN=5: Cyclic sleep mode. After data processing is complete upon wakeup, the system stays
     #                in IDLE state for 2s.
     #   AT+CFUN=6: Cyclic sleep mode. After data processing is complete upon wakeup, the system stays
     #                in IDLE state for 10 minutes. For other tasks, after message processing is
     #                complete and the system is IDLE again, the system automatically enters SLEEP mode
     #                again.
     #   AT+CFUN=7: Cyclic sleep mode. After data processing is complete upon wakeup, the system stays
     #                in IDLE state for 2s. For other tasks, after message processing is complete and
     #                the system is IDLE again, the system automatically enters SLEEP mode again. During
     #                wakeup, the serial port can work properly.
     #   AT+CFUN=8: Cyclic sleep mode. After data processing is complete upon wakeup, the system stays
     #                in IDLE state for 10 minutes. For other tasks, after message processing is
    #                complete and the system is IDLE again, the system automatically enters SLEEP mode
    #                again. Same as AT+CFUN=6.
    #   AT+CFUN=9: Cyclic sleep mode. After data processing is complete upon wakeup, the system stays
    #                in IDLE state for a period (2s by default), which is configurable.
    #                AT^SCFG="PowerSaver/Mode9/Timeout",<psm9to>;
    #                RTS0 and RTS1 can function as wakeup sources. Wakeup can be activated through RTS0
    #                and RTS1.
    Init1 = AT+CFUN=1

    [Dialer modem-stop]
    Init1 = AT+CFUN=0

    [Dialer info-at]
    # Get list of AT commands.
    Init3 = AT+CLAC

    [Dialer info-scan]
    # Get a list of available operators.
    # <status>,<operator_alphanumeric_format>,<operator_numeric_format>,<?>,<?>,<?>
    #  <status>:
    #        0 -- Unknown
    #        1 -- Available
    #        2 -- Current
    #        3 -- Forbidden
    Init3 = AT+COPS=?
    #Init2 = AT+CFUN=1
    #Init4 = AT+COPS=?
    #Init5 = AT+CFUN=1

    [Dialer info-gsm]
    # Get info about the current operator.
    Init4 = AT+COPS?

    # Get the radio signal strength.
    # <Signal>,<RSSI>,<RSRP>,<SINR>,<RSRQ>
    # RSSI -- Received Signal Strength Indicator (only for LTE).
    # RSRP -- Reference Signal Receive Power
    # SINR -- Signalto-Interference-Plus-noise Ratio
    # RSRQ -- Reference Signal Received Quality
    #
    #---------------------------------------------------------------
    # 0 RSSI < –120 dBm            | 0 RSRP < –140 dBm             | RSSI formula:
    # 1 –120 dBm ≤ RSSI < –119 dBm | 1 –140 dBm ≤ RSRP < – 139 dBm |   dBm= value1 -120
    # 2 –119 dBm ≤ RSSI < –118 dBm | 2 –139 dBm ≤ RSRP < –138 dBm  | RSRP formula:
    # ...                          | ...                           |   dBm= value2 -140
    # 53 –68 dBm ≤ RSSI < –67 dBm  | 45 -96 dBm ≤ RSRP < –95 dBm   |
    # ...                          | ...                           | RSSI < -87 = bad
    # 94 –27 dBm ≤ RSSI < –26 dBm  | 95 –46 dBm ≤ RSRP < –45 dBm   | RSRP < -91 = bad
    # 95 –26 dBm ≤ RSSI < –25 dBm  | 96 –45 dBm ≤ RSRP < –44 dBm   |
    #                              | 97 –44 dBm ≤ RSRP             |
    #                              | 255 unknown or undetectable   |
    #---------------------------------------------------------------
    # 0 SINR < –20 dB              | 0 RSRQ < –19.5 dB             | SINR formula:
    # 1 –20 dB ≤ SINR < –19.8 dB   | 1 –19.5 dB ≤ RSRQ < –19 dB    |   dB= 0.2 x value3 -20
    # 2 –19.8 dB ≤ SINR < –19.6 dB | 2 –19 dB ≤ RSRQ < –18.5 dB    | RSRQ formula:
    # ...                          | ...                           |   dB= 0.5 x value4 -19.5
    # 181 16 dB ≤ SINR < 16.2 dB   | 18 –11 dB ≤ RSRQ < –10.5 dB   |
    # ...                          | ...                           | SINR <   0 = bad
    # 249 29.6 dB ≤ SINR < 29.8 dB | 32 –4 dB ≤ RSRQ < –3.5 dB     | RSRQ < -16 = bad
    # 250 29.8 dB ≤ SINR < 30 dB   | 33 –3.5 dB ≤ RSRQ < –3 dB     |
    # 251 30 dB ≤ SINR             | 34 –3 dB ≤ RSRQ               |
    # 255 unknown or undetectable  | 255 unknown or undetectable   |
    #--------------------------------------------------------------|
    Init5 = AT^HCSQ?

    [Dialer modem-reboot]
    Init3 = AT^RESET

    [Dialer info-device]
    # +CGMI   -- manufacturer,
    # +CGMM   -- model number,
    # +CGSN   -- IMEI number (International Mobile Equipment Identity)
    # +CIMI   -- IMSI number (International Mobile Subscriber Identity)
    # +CGMR   -- software version
    # +CPAS   -- mobile phone activity status
    # +CBC    -- battery charge level and battery charging status
    # +CREG   -- mobile network registration status
    # +CNUM   -- MSISDN number (Mobile Station International Subscriber Directory Number), phone number
    # ^ICCID? -- SIM card serial number
    #Init4 = AT+CGMI;+CGMM;+CGSN;+CIMI;+CGMR;+CPAS;+CBC;^ICCID?
    Init4 = ATI
    # Display the current configuration of the device.
    Init5 = AT^SETPORT=?;^SETPORT?
    # Display the currently active modem mode.
    Init6 = AT^GETPORTMODE

    [Dialer info-config]
    Init4 = AT^SYSCFG=?;^SYSCFG?
    Init5 = AT^SYSCFGEX=?;^SYSCFGEX?
    Init6 = AT^SYSINFO
    Init7 = AT^SYSINFOEX

    [Dialer set-old]
    # AT^SYSCFG=<mode>,<acqorder>,<band>,<roam>,<srvdomain>
    #      <mode>:
    #        2 -- auto
    #       13 -- only GSM (2G)
    #       14 -- only WCDMA/UMTS (3G)
    #       16 -- no changes
    #  <acqorder>:
    #        0 -- auto searching
    #        1 -- first GSM, then WCDMA
    #        2 -- first WCDMA, then GSM
    #        3 -- no changes
    #      <band>: (HEX values. All of them except the first and the last can be added.)
    # 3FFFFFFF -- All Bands
    # 00080000 -- GSM 850
    # 00000080 -- GSM DCS systems 1800
    # 00000100 -- Extended GSM 900
    # 00000200 -- Primary GSM 900
    # 00100000 -- Railway GSM 900
    # 00200000 -- GSM PCS 1900
    # 00400000 -- WCDMA IMT 2000
    # 00800000 -- WCDMA II PCS 1900
    # 04000000 -- WCDMA V 850
    # 0002000000000000 -- WCDMA VIII 900
    # 40000000 -- no changes
    #      <roam>:
    #        0 -- roaming disabled
    #        1 -- roaming enabled
    #        2 -- no changes
    # <srvdomain>: (PS (data), CS (sms, voice)
    #        0 -- CS_ONLY
    #        1 -- PS_ONLY
    #        2 -- CS_PS
    #        3 -- ANY
    #        4 -- no changes
    #
    Init4 = AT^SYSCFG=2,0,3FFFFFFF,1,2

    [Dialer set-new]
    # AT^SYSCFGEX=<acqorder>,<band>,<roam>,<srvdomain>,<lteband>,<reserve1>,<reserve2>
    #  <acqorder>: (All of the values except the first and the last one can be connected)
    #        00 -- auto
    #        01 -- GSM (2G)
    #        02 -- WCDMA/UMTS (3G)
    #        03 -- LTE (4G)
    #        99 -- no change
    #      <band>:
    #        80 -- GSM1800
    #       300 -- GSM900
    #     80000 -- GSM850
    #    200000 -- GSM1900
    #    400000 -- UTMS B1 (2100)
    #    800000 -- UTMS B2 (1900)
    #   4000000 -- UTMS B5 (850)
    # 2000000000000 -- UTMS B8 (900)
    #         1 -- BC0A
    #         2 -- BC0B
    #         4 -- BC1
    #         8 -- BC2
    #        10 -- BC3
    #        20 -- BC4
    #        40 -- BC5
    #       400 -- BC6
    #       800 -- BC7
    #      1000 -- BC8
    #      2000 -- BC9
    #      4000 -- BC10
    #      8000 -- BC11
    #  10000000 -- BC12
    #  20000000 -- BC13
    #  80000000 -- BC14
    #  3FFFFFFF -- All Bands
    #      <roam>:
    #        0 -- roaming disabled
    #        1 -- roaming enabled
    #        2 -- no changes
    # <srvdomain>: (PS (data), CS (sms, voice)
    #        0 -- CS_ONLY
    #        1 -- PS_ONLY
    #        2 -- CS_PS
    #        3 -- ANY
    #        4 -- no changes
    #  <lteband>: (HEX values, can be added)
    #        1              LTE  B1 (FDD 2100 MHz)
    #        4              LTE  B3 (FDD 1800 MHz)
    #        40             LTE  B7 (FDD 2600 MHz)
    #        80             LTE  B8 (FDD 900)
    #        2000           LTE B13 (FDD 700 c MHz)
    #        20000          LTE B17 (FDD 700 bc MHz)
    #        80000          LTE B20 (FDD 800 dd MHz)
    #        2000000000     LTE B38 (TDD 2600 MHz)
    #        8000000000     LTE B40 (TDD 2300 MHz)
    #        800C5          LTE EU  (Band 1, 3, 7, 8, 20)
    #        800D5          LTE EU/Asia/Africa (Band 1, 3, 5, 7, 8, 20)
    #        10000000000    LTE B40 (TDD 2300 MHz)
    #        40000000       no changes
    #        7FFFFFFFFFFFFFFF   All Bands
    #  <reserve1>: (for future use, set empty)
    #  <reserve2>: (for future use, set empty)
    #
    Init4 = AT^SYSCFGEX="030201",3FFFFFFF,1,2,7FFFFFFFFFFFFFFF,,
            ''',
     'user': 'root',
     'group': 'root',
     'mode': 0o640,
    }]



def installSupport(root, info):
    print('... Installing Dlink Support')
    for element in elements:
        utils.installElem(root, element, info)


