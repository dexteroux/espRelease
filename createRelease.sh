cp ~/espAutoLoader/esp_timer/build/esp_timer_example.bin               images/esp_timer_example.bin 
cp ~/espAutoLoader/esp_timer/build/bootloader/bootloader.bin           images/bootloader/bootloader.bin 
cp ~/espAutoLoader/esp_timer/build/partition_table/partition-table.bin images/partition_table/partition-table.bin 
cp ~/espAutoLoader/esp_timer/build/ota_data_initial.bin                images/ota_data_initial.bin

gocryptfs ./distribution/cryptfs ./distribution/open
pushd ./distribution/open
rsync -azP --exclude "build" /home/pi/espAutoLoader/esp_timer ./
rsync -azP /home/www-data/web2py/applications/client ./
rm -rf ./client/databases/* ./client/errors/* ./client/sessions/*
popd
sudo umount ./distribution/open

