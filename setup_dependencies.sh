#!/bin/bash
echo -----------------------------------------------------------
echo Updating System -------------------------------------------
echo -----------------------------------------------------------
sudo apt-get update

echo -----------------------------------------------------------
echo Verifying dependencies ------------------------------------
echo -----------------------------------------------------------
sudo apt-get install -y git  cmake  sdcc  guile-2.0-dev  guile-2.0-doc  ccache  python-all-dev  python3-all-dev  swig  swig-doc  libfftw3-dev  libcppunit-dev  libboost-all-dev  libgsl0-dev  libusb-dev libasound2-dev  python-numpy  python3-numpy  python-cheetah  python-mako  python-wxgtk2.8  python-qwt5-qt4 libqwt5-qt4-dev  libfontconfig1-dev  libxrender-dev  libxi-dev  libsdl1.2-dev  python-scipy python3-scipy  python-matplotlib  python3-matplotlib  doxygen gpsd python-gps gpsd-clients python-pip
./dependencias_gnuradio.sh
sudo apt-get install -y libqwt-dev
sudo pip install -U scikit-learn

echo -----------------------------------------------------------
echo Installing uhd --------------------------------------------
echo -----------------------------------------------------------
./uhd_install.sh

echo -----------------------------------------------------------
echo Installing GNU Radio --------------------------------------
echo -----------------------------------------------------------
git clone git://git.gnuradio.org/gnuradio
cd gnuradio
git submodule init
git submodule update
mkdir build
cd build
cmake ../
make -j8
sudo make install
cd ..
cd ..

echo -----------------------------------------------------------
echo Installing GNU Radio Depencencies--------------------------
echo -----------------------------------------------------------
tar -xzf dependencies.tar.gz
cd dependencies
cd ./gr-foo
mkdir build
cd build
cmake ../
make -j8
sudo make install
cd ..
cd ..

cd ./gr-ieee802-15-4
mkdir build
cd build
cmake ../
make -j8
sudo make install
cd ..
cd ..

cd ./gr-eventstream
mkdir build
cd build
cmake ../
make -j8
sudo make install
cd ..
cd ..

cd ./gr-uhdgps
mkdir build
cd build
cmake ../
make -j8
sudo make install
cd ..
cd ..

cd ./fann
mkdir build
cd build
cmake ../
make -j8
sudo make install
cd ..
cd ..

sudo pip install fann2
sudo ldconfig
echo -----------------------------------------------------------
echo Script Finished -------------------------------------------
echo -----------------------------------------------------------
