#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python
export GR_CONF_CONTROLPORT_ON=False
export PATH=/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/python:$PATH
export LD_LIBRARY_PATH=/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/build/swig:$PYTHONPATH
/usr/bin/python2 /home/sbrc17/Documents/FrameworkCRN/gr-pmt_cpp/python/qa_message_type.py 
