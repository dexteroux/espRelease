sudo apt install modemmanager network-manager dnsutils ntpstat
sudo apt purge openresolv dhcpcd5
sudo mmcli --list-modems
sudo cp NetworkManager.conf /etc/NetworkManager/NetworkManager.conf

sudo nmcli connection del 'bsnl' 
sudo nmcli connection del 'jio' 
sudo nmcli connection del 'AndroidLink'
sudo nmcli connection del 'kitaabikeeda_EXT'
sudo nmcli connection del 'eth0'
sudo nmcli connection del 'eth1'

#sudo nmcli connection add type gsm ifname '*' con-name 'jio' apn 'jionet' gsm.home-only no connection.autoconnect yes ipv6.route-metric 100 ipv4.route-metric 100
sudo nmcli connection add type gsm      ifname '*'  con-name 'bsnl'             apn 'bsnlstatic' gsm.home-only no connection.autoconnect yes ipv4.route-metric 100 
sudo nmcli connection add type wifi     ifname '*'  con-name 'AndroidLink'      ssid "AndroidLink"      wifi-sec.key-mgmt wpa-psk wifi-sec.psk "12345678"         ipv4.route-metric 500 
sudo nmcli connection add type wifi     ifname '*'  con-name 'kitaabikeeda_EXT' ssid "kitaabikeeda_EXT" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "anirudhkahaanhai" ipv4.route-metric 500
sudo nmcli connection add type ethernet ifname eth1 con-name 'eth1' ipv4.method auto
sudo nmcli connection add type ethernet ifname eth0 con-name 'eth0' ipv4.method shared ipv4.address 192.168.100.1/24 ipv4.gateway 192.168.100.1 connection.autoconnect yes ipv4.route-metric 900   



