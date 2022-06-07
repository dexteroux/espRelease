sudo systemctl stop monitor.timer
sudo systemctl stop monitor.service
./espBoot.py
. /home/pi/esp/esp-idf/export.sh
esptool.py --chip esp32 -p /dev/ttyS0 -b 460800 --before=default_reset --after=hard_reset write_flash --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 bootloader.bin 0x20000 esp_timer_example.bin 0xe000 ./partition-table.bin 0x16000 ota_data_initial.bin
./espRst.py
sudo systemctl start monitor.timer
sudo systemctl list-timers
