cp /home/pi/src/build/esp_timer_example.bin               images/esp_timer_example.bin 
cp /home/pi/src/build/bootloader/bootloader.bin           images/bootloader/bootloader.bin 
cp /home/pi/src/build/partition_table/partition-table.bin images/partition_table/partition-table.bin 
cp /home/pi/src/build/ota_data_initial.bin                images/ota_data_initial.bin

gocryptfs ./distribution/cryptfs ./distribution/open
cd ./distribution/open
rsync -azP --exclude "build" /home/pi/src/ ./esp_timer
rsync -azP /home/www-data/web2py/applications/client ./
rm -rf ./client/databases/* ./client/errors/* ./client/sessions/*
cd ../..
sudo umount ./distribution/open

