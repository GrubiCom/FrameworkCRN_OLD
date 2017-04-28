#!/bin/bash

THREADS=`getconf _NPROCESSORS_ONLN`

echo -----------------------------------------------------------
echo -------------- Installing FrameworkCRN --------------------
echo -----------------------------------------------------------
cd gr-pmt_cpp/
mkdir build
cd build/
cmake ../
make -j$THREADS && \
sudo make install
sudo ldconfig
cd ..
cd ..

sudo mkdir /opt/FrameworkCRN
sudo cp gr-pmt_cpp/python/final_data_config3.net /opt/FrameworkCRN/final_data_config.net
sudo chown -R root.users /opt/FrameworkCRN
sudo chmod -R 0755 /opt/FrameworkCRN

echo -----------------------------------------------------------
echo -------------- Building FrameworkCRN Blocks ---------------
echo -----------------------------------------------------------
grcc dependencies/gr-ieee802-15-4/examples/ieee802_15_4_OQPSK_PHY.grc
grcc gr-pmt_cpp/grc/get_power.grc
grcc gr-pmt_cpp/grc/file_recorder.grc
grcc gr-pmt_cpp/grc/802.15.4_Cog.grc
grcc gr-pmt_cpp/grc/sbrc17/mobility_master.grc
grcc gr-pmt_cpp/grc/sbrc17/share_master.grc
grcc gr-pmt_cpp/grc/sbrc17/decision.grc
grcc gr-pmt_cpp/grc/sbrc17/sense_master.grc
grcc gr-pmt_cpp/grc/sbrc17/usrp.grc
grcc gr-pmt_cpp/grc/sbrc17/usrp_master.grc
grcc gr-pmt_cpp/grc/sbrc17/mobility.grc
grcc gr-pmt_cpp/grc/sbrc17/sense.grc
grcc gr-pmt_cpp/grc/sbrc17/send_data_sense.grc
grcc gr-pmt_cpp/grc/sbrc17/share.grc
grcc gr-pmt_cpp/grc/sbrc17/slave.grc
grcc gr-pmt_cpp/grc/sbrc17/master.grc
