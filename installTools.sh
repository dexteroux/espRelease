sudo apt update 
sudo apt install vim git wget flex bison gperf python3 python3-pip python3-setuptools cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0 byobu
mkdir -p ~/esp
pushd ~/esp
git clone --recursive https://github.com/espressif/esp-idf.git
popd
pushd ~/esp/esp-idf
git fetch
git checkout v4.3.1
git submodule update --init --recursive
./install.sh esp32
popd
