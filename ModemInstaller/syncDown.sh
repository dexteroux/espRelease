sudo rsync -r -a -v -z -e "ssh -p8022" --delete pi@localhost:/home/pi/archives/ /var/cache/apt/archives
sudo apt update
sudo apt upgrade
