#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/lib
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/lib:$PATH
export LD_LIBRARY_PATH=/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-pmt_cpp 
