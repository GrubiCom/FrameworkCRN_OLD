#!/bin/bash


grcc dependence/gr-ieee802-15-4/examples/ieee802_15_4_OQPSK_PHY.grc

grcc /gr-pmt_cpp/grc/802.15.4_Cog.grc

grcc gr-pmt_cpp/grc/sbrc17/mobility_master.grc
grcc gr-pmt_cpp/grc/sbrc17/share_master.grc
grcc gr-pmt_cpp/grc/sbrc17/decision.grc
grcc gr-pmt_cpp/grc/sbrc17/sense_master.grc
grcc gr-pmt_cpp/grc/sbrc17/usrp.grc

grcc gr-pmt_cpp/grc/sbrc17/mobility.grc
grcc gr-pmt_cpp/grc/sbrc17/sense.grc
grcc gr-pmt_cpp/grc/sbrc17/send_data_sense.grc
grcc gr-pmt_cpp/grc/sbrc17/share.grc
grcc gr-pmt_cpp/grc/sbrc17/slave.grc
grcc gr-pmt_cpp/grc/sbrc17/master.grc
