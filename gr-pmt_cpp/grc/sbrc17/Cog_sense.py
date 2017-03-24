#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Cognitive network over IEEE 802.15.4
# Author: Ariel Marques
# Generated: Wed Dec 21 11:18:22 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from IEEE_802_15_4 import IEEE_802_15_4  # grc-generated hier_block
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
from send_data_sense import send_data_sense  # grc-generated hier_block
from spectrum_mobitily import spectrum_mobitily  # grc-generated hier_block
from spectrum_sensing import spectrum_sensing  # grc-generated hier_block
from spectrum_sharing import spectrum_sharing  # grc-generated hier_block
from usrp import usrp  # grc-generated hier_block
import pmt_cpp
import wx


class Cog_sense(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Cognitive network over IEEE 802.15.4")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.bw = bw = 1000e3

        ##################################################
        # Blocks
        ##################################################
        self.usrp_0 = usrp()
        self.spectrum_sharing_0 = spectrum_sharing()
        self.spectrum_sensing_0 = spectrum_sensing()
        self.spectrum_mobitily_0 = spectrum_mobitily()
        self.send_data_sense_0 = send_data_sense()
        self.pmt_cpp_transmission_data_0 = pmt_cpp.transmission_data()
        self.pmt_cpp_pmt_extract2_0 = pmt_cpp.pmt_extract2()
        self.IEEE_802_15_4_0 = IEEE_802_15_4()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.IEEE_802_15_4_0, 'rxout'), (self.pmt_cpp_pmt_extract2_0, 'in_pdu'))    
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'info_neighbor'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'Ack'), (self.send_data_sense_0, 'Ack'))    
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'sense'), (self.spectrum_sensing_0, 'sense'))    
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'share'), (self.spectrum_sharing_0, 'sharing_message'))    
        self.msg_connect((self.pmt_cpp_transmission_data_0, 'packet'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_transmission_data_0, 'signal_out'), (self.spectrum_mobitily_0, 'signal'))    
        self.msg_connect((self.send_data_sense_0, 'repeat_message'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.send_data_sense_0, 'message'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.spectrum_mobitily_0, 'ccc'), (self.usrp_0, 'command_source'))    
        self.msg_connect((self.spectrum_sensing_0, 'file_ready'), (self.send_data_sense_0, 'file_ready'))    
        self.msg_connect((self.spectrum_sensing_0, 'sense_tune_command'), (self.usrp_0, 'command_source'))    
        self.msg_connect((self.spectrum_sharing_0, 'bool'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.spectrum_sharing_0, 'bool'), (self.pmt_cpp_transmission_data_0, 'signal_in'))    
        self.msg_connect((self.spectrum_sharing_0, 'bool'), (self.spectrum_mobitily_0, 'flag'))    
        self.msg_connect((self.spectrum_sharing_0, 'new_freq'), (self.usrp_0, 'command_source'))    
        self.msg_connect((self.spectrum_sharing_0, 'new_freq'), (self.usrp_0, 'command_sink'))    
        self.connect((self.IEEE_802_15_4_0, 0), (self.usrp_0, 0))    
        self.connect((self.usrp_0, 0), (self.IEEE_802_15_4_0, 0))    
        self.connect((self.usrp_0, 0), (self.spectrum_mobitily_0, 0))    
        self.connect((self.usrp_0, 0), (self.spectrum_sensing_0, 0))    

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw


def main(top_block_cls=Cog_sense, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
