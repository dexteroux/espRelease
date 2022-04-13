DEVICE_IP=192.168.2.105
echo " sync esp"
rsync -azP /home/pi/esp/            pi@${DEVICE_IP}:/home/pi/esp
echo " sync espAutoLoader"
rsync -azP /home/pi/espAutoLoader/  pi@${DEVICE_IP}:/home/pi/espAutoLoader
echo " sync espRelease"
rsync -azP /home/pi/espRelease/     pi@${DEVICE_IP}:/home/pi/espRelease
echo " sync archives"
rsync -azP /home/pi/archives/       pi@${DEVICE_IP}:/home/pi/archives
echo " sync .espressif"
rsync -azP /home/pi/.espressif/     pi@${DEVICE_IP}:/home/pi/.espressif 

#rsync -azPq /home/pi/esp/            pi@${DEVICE_IP}:/home/pi/esp
#rsync -azPq /home/pi/espAutoLoader/  pi@${DEVICE_IP}:/home/pi/espAutoLoader
#rsync -azPq /home/pi/espRelease/     pi@${DEVICE_IP}:/home/pi/espRelease
#rsync -azPq /home/pi/archives/       pi@${DEVICE_IP}:/home/pi/archives
#rsync -azPq /home/pi/.espressif/     pi@${DEVICE_IP}:/home/pi/.espressif 
