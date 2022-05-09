sudo apt install modemmanager network-manager dnsutils ntpstat
mmcli --list-modems
sudo nmcli connection add type gsm ifname '*' con-name 'jio' apn 'jionet' gsm.home-only no connection.autoconnect yes ipv6.route-metric 100
nmcli dev wifi connect kitaabikeeda_EXT password "anirudhkahaanhai"
