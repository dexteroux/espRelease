#!/bin/bash
##type lsusb to find "vendor" and "product" ID in terminal
#set -euo pipefail
#IFS=$'\n\t'

##edit the below tow lines of vendor and product values using lsusb result
#dev=$(lsusb -t | grep huawei_cdc_ncm | grep 'If 2' | cut -d' ' -f13|cut -d"," -f1)
##VENDOR=05a3
##PRODUCT=9230
#echo ${dev}
#lsusb -s $dev
#VENDOR=$(lsusb -s $dev | cut -d' ' -f6 | cut -d: -f1)
#echo ${VENDOR}
#PRODUCT=$(lsusb -s $dev | cut -d' ' -f6 | cut -d: -f2)
#echo ${PRODUCT}
#for DIR in $(find /sys/bus/usb/devices/ -maxdepth 1 -type l); do
#	if [[ -f $DIR/idVendor && -f $DIR/idProduct &&
#		$(cat $DIR/idVendor) == $VENDOR && $(cat $DIR/idProduct) == $PRODUCT ]]; then
#		echo ${DIR}/authorized
#		echo 0 > $DIR/authorized
#		sleep 0.5
#		echo 1 > $DIR/authorized
#	fi
#done

MODEM=$(mmcli --list-modems)
echo ${MODEM}
if [[ ${MODEM} == *"huawei"* ]]
then
	echo "Modem present !!"
else
	echo "Modem not present !!"
	echo "Resetting USB hub ..."
	sudo uhubctl -a off
	sleep 10
	sudo uhubctl -a on
	sleep 10
	sudo uhubctl -a off
	echo "Resetting USB hub done"
fi


