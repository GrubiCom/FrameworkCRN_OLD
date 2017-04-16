#!/bin/bash
sudo apt-get update
cd gr-pmt_cpp/
mkdir build
cd build/
cmake ../
make -j8
sudo make install
sudo ldconfig

