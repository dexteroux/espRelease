sudo apt install modemmanager network-manager dnsutils ntpstat
sudo apt purge openresolv dhcpcd5
sudo mmcli --list-modems
sudo cp ./NetworkManager.conf /etc/NetworkManager/NetworkManager.conf
#sudo nmcli connection add type gsm ifname '*' con-name 'jio' apn 'jionet' gsm.home-only no connection.autoconnect yes ipv6.route-metric 100 ipv4.route-metric 100
sudo nmcli connection add type gsm ifname '*' con-name 'bsnl' apn 'bsnlstatic' gsm.home-only no connection.autoconnect yes ipv4.route-metric 100 
#nmcli dev wifi connect kitaabikeeda_EXT password "anirudhkahaanhai"
#sudo nmcli dev wifi connect AndroidLink password "12345678" ipv4.route-metric 500 
sudo nmcli connection add type wifi ssid "AndroidLink" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "12345678" ipv4.route-metric 500 
#sudo nmcli con add con-name eth1 type ethernet ifname eth1 ipv4.method manual ipv4.address 192.168.1.100/24 ipv4.gateway 192.168.1.1 connection.autoconnect yes ipv4.route-metric 200
sudo nmcli connection add type wifi ssid "kitaabikeeda_EXT" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "anirudhkahaanhai" ipv4.route-metric 500                                               
sudo nmcli con add con-name eth1 type ethernet ifname eth1 ipv4.method auto
sudo nmcli con add con-name eth0 type ethernet ifname eth0 ipv4.method shared ipv4.address 192.168.100.1/24 ipv4.gateway 192.168.100.1 connection.autoconnect yes ipv4.route-metric 900   



