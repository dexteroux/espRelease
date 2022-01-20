sudo systemctl stop web2pyClientSched.service
sudo -u www-data /usr/bin/python3 /home/www-data/web2py/web2py.py -K client
