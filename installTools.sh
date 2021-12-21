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
