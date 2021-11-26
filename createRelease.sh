cp ~/devel/espAutoLoader/esp_timer/build/esp_timer_example.bin               images/esp_timer_example.bin 
cp ~/devel/espAutoLoader/esp_timer/build/bootloader/bootloader.bin           images/bootloader/bootloader.bin 
cp ~/devel/espAutoLoader/esp_timer/build/partition_table/partition-table.bin images/partition_table/partition-table.bin 
cp ~/devel/espAutoLoader/esp_timer/build/ota_data_initial.bin                images/ota_data_initial.bin

rsync -azP /home/www-data/web2py/applications/client/ ./client
rm -rf client/databases/* client/errors/* rm -rf client/sessions/*

