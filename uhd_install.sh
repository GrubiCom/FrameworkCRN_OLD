#!/bin/bash
sudo apt-get update
cd $HOME
git clone https://github.com/EttusResearch/uhd
cd uhd
git checkout release_003_008_000
cd host
mkdir build
cd build
cmake ../
make -j8
sudo make install
sudo ldconfig
sudo "/usr/local/lib/uhd/utils/uhd_images_downloader.py"
cd $HOME/uhd/host/utils
sudo cp uhd-usrp.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
