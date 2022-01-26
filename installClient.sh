
mkdir -p ./distribution/open
gocryptfs ./distribution/cryptfs ./distribution/open
cd ./distribution/open

rsync -azP ./client/ /home/www-data/web2py/applications/client
cp ./routes.py /home/www-data/web2py/
cp ./web2pyClientSched.service /etc/systemd/system/web2pyClientSched.service

chown -R www-data:www-data /home/www-data/web2py/applications/client
systemctl enable web2pyClientSched.service
systemctl restart web2pyClientSched.service
systemctl restart apache2.service

cd ../..
sudo umount ./distribution/open
