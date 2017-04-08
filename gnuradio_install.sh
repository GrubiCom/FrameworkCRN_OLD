#!/bin/bash
sudo apt-get update
cd $HOME
git clone --recursive https://github.com/gnuradio/gnuradio
cd gnuradio
git checkout v3.7.7.2
mkdir build
cd build
cmake ../
make -j8
sudo make install
sudo ldconfig
