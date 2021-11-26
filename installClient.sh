rsync -azP ./client/ /home/www-data/web2py/applications/client
cp ./routes.py /home/www-data/web2py/
chown -R www-data:www-data /home/www-data/web2py/applications/client
cp ./web2pyClientSched.service /etc/systemd/system/web2pyClientSched.service
systemctl enable web2pyClientSched.service
systemctl restart web2pyClientSched.service
systemctl restart apache2.service
