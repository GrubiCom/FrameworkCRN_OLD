#!/bin/bash

UHD_URL="https://github.com/EttusResearch/uhd"
GNURADIO_URL="https://github.com/gnuradio/gnuradio"

THREADS=`getconf _NPROCESSORS_ONLN`

echo -----------------------------------------------------------
echo --------------------- Updating System ---------------------
echo -----------------------------------------------------------
sudo apt-get update

echo -----------------------------------------------------------
echo ------------------ Verifying Dependecies ------------------
echo -----------------------------------------------------------
# Removed git-core guile-2.0-doc swig-doc libcppunit-doc libfftw3-doc python-numpy-doc qt4-doc python-qt4-doc
sudo apt-get install -y git cmake sdcc guile-2.0-dev ccache python-all-dev python3-all-dev swig libfftw3-dev libfftw3-bin libcppunit-dev libcppunit-1.13-0 libboost-all-dev libgsl0-dev libusb-dev libusb-1.0-0 libusb-1.0-0-dev libasound2-dev python-numpy python-numpy-dbg python3-numpy python-cheetah python-mako python-wxgtk2.8 python-qwt5-qt4 libqwt5-qt4-dev libfontconfig1-dev libxrender-dev libxi-dev libsdl1.2-dev python-scipy python3-scipy python-matplotlib python3-matplotlib doxygen gpsd python-gps gpsd-clients python-pip build-essential libtool libudev-dev libncurses5-dev libncurses5 libncurses5-dbg ncurses-bin cpufrequtils python-docutils qt4-bin-dbg qt4-default libqt4-dev libqt4-dev-bin python-qt4 python-qt4-dbg python-qt4-dev libpulse-dev g++ automake autoconf python-dev fort77 python-opengl python-lxml qt4-dev-tools libqwtplot3d-qt4-dev pyqt4-dev-tools wget gtk2-engines-pixbuf r-base-dev python-tk liborc-0.4-0 liborc-0.4-dev python-gtk2 libzmq1 libzmq-dev python-requests python-sphinx libcomedi-dev libfann-dev
# NOTE: libqwt-dev Breaks: libqwt5-qt4-dev

sudo pip install -U scikit-learn

echo -----------------------------------------------------------
echo ---------------------- Installing UHD ---------------------
echo -----------------------------------------------------------
git clone $UHD_URL

if [ $? != 0 ]; then
	
	echo "Error getting UHD driver, check UHD_URL"
	exit 1
fi

cd uhd
git checkout release_003_008_000
cd host
mkdir build
cd build
cmake ../
make -j$THREADS && \
sudo make install
ldconfig
/usr/local/lib/uhd/utils/uhd_images_downloader.py
cp ../utils/uhd-usrp.rules /etc/udev/rules.d/
udevadm control --reload-rules
udevadm trigger

echo -----------------------------------------------------------
echo ------------------ Installing GNU Radio -------------------
echo -----------------------------------------------------------
git clone $GNURADIO_URL

if [ $? != 0 ]; then
	
	echo "Error downloading GNU Radio, check GNURADIO_URL"
	exit 1
fi

cd gnuradio
git submodule init
git submodule update
mkdir build
cd build
cmake ../
make -j$THREADS
sudo make install
cd ..
cd ..

echo -----------------------------------------------------------
echo ------------ Installing Framework Dependencies ------------
echo -----------------------------------------------------------
tar -xf dependencies.tar.gz
cd dependencies
cd ./gr-foo
mkdir build
cd build 
cmake ../
make -j$THREADS && \
sudo make install
cd ..
cd ..

cd ./gr-ieee802-15-4
mkdir build
cd build
cmake ../
make -j$THREADS && \
sudo make install
cd ..
cd ..

cd ./gr-eventstream
mkdir build
cd build
cmake ../
make -j$THREADS && \
sudo make install
cd ..
cd ..

cd ./gr-uhdgps
mkdir build
cd build
cmake ../
make -j$THREADS && \
sudo make install
cd ..
cd ..

# cd ./fann
# mkdir build
# cd build
# cmake ../
# make -j$THREADS && \
# sudo make installn
# cd ..
# cd ..

# pip install fann2
# ldconfig

echo -----------------------------------------------------------
echo ------------ GNU Radio Installation Complete! -------------
echo -----------------------------------------------------------