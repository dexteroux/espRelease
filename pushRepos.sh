DEVICE_IP=192.168.2.108

rsync -azPq /home/pi/esp/            pi@${DEVICE_IP}:/home/pi/esp
rsync -azPq /home/pi/espAutoLoader/  pi@${DEVICE_IP}:/home/pi/espAutoLoader
rsync -azPq /home/pi/espRelease/     pi@${DEVICE_IP}:/home/pi/espRelease
rsync -azPq /home/pi/archives/       pi@${DEVICE_IP}:/home/pi/archives
rsync -azPq /home/pi/.espressif/     pi@${DEVICE_IP}:/home/pi/.espressif 
