rm -rf release
tar zxvf release.tar.gz
pushd release
./flash.sh
popd
cp ./release/flashInstaller.sh ./
