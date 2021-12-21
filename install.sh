#esptool.py --chip ESP32 -p /dev/ttyS0 -b 460800 --before=no_reset --after=no_reset write_flash --flash_mode dio --flash_freq 40m --flash_size 2MB 0x8000 images/partition_table/partition-table.bin 0x1000 images/bootloader/bootloader.bin 0x10000 images/esp_timer_example.bin

. ~/esp/esp-idf/export.sh 
esptool.py --chip ESP32 -p /dev/ttyS0 -b 460800 --before=no_reset --after=no_reset write_flash --flash_mode dio --flash_freq 40m --flash_size 16MB 0x8000 images/partition_table/partition-table.bin 0xd000 images/ota_data_initial.bin 0x1000 images/bootloader/bootloader.bin 0x10000 images/esp_timer_example.bin


