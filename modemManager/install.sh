sudo mkdir -p /etc/indra
sudo cp resetModem.sh /etc/indra/
sudo cp resetModem.timer /etc/systemd/system/
sudo cp resetModem.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start resetModem.timer 
sudo systemctl enable resetModem.timer
