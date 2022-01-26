
mkdir -p ./distribution/open
gocryptfs ./distribution/cryptfs ./distribution/open
cd ./distribution/open

rsync -azP ./client/ /home/www-data/web2py/applications/client
rsync -azP ./esp_timer/ /home/pi/src
cp ./routes.py /home/www-data/web2py/
cp ./web2pyClientSched.service /etc/systemd/system/web2pyClientSched.service

chown -R www-data:www-data /home/www-data/web2py/applications/client
chown -R pi:pi /home/pi/src
systemctl enable web2pyClientSched.service
systemctl restart web2pyClientSched.service
systemctl restart apache2.service

cd ../..
sudo umount ./distribution/open
