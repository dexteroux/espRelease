sudo apt install modemmanager network-manager dnsutils ntpstat
mmcli --list-modems
sudo nmcli connection add type gsm ifname '*' con-name 'jio' apn 'jionet' gsm.home-only no connection.autoconnect yes ipv6.route-metric 100 ipv4.route-metric 100
nmcli dev wifi connect kitaabikeeda_EXT password "anirudhkahaanhai"
sudo nmcli con add con-name eth0 type ethernet ifname eth0 ipv4.method manual ipv4.address 192.168.1.1/24 ipv4.gateway 192.168.1.100 connection.autoconnect yes ipv4.route-metric 900

