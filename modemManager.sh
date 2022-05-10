sudo apt install modemmanager network-manager dnsutils ntpstat
mmcli --list-modems
sudo nmcli connection add type gsm ifname '*' con-name 'jio' apn 'jionet' gsm.home-only no connection.autoconnect yes ipv6.route-metric 100
nmcli dev wifi connect kitaabikeeda_EXT password "anirudhkahaanhai"
sudo nmcli connection add type ethernet connection.interface-name eth0 connection.id  "Ethernet" ip4 192.168.1.1/24 gw4 192.168.1.10
