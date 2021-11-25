rsync -azP ./client/ /home/www-data/web2py/applications/client
cp ./routes.py /home/www-data/web2py/
chown -R www-data:www-data /home/www-data/web2py/applications/client
