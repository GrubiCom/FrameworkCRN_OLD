#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver using OQPSK PHY
# Generated: Wed Mar 29 16:57:43 2017
##################################################

# Call XInitThreads as the _very_ first thing.
# After some Qt import, it's too late
import ctypes
import sys
if sys.platform.startswith('linux'):
    try:
        x11 = ctypes.cdll.LoadLibrary('libX11.so')
        x11.XInitThreads()
    except:
        print "Warning: failed to XInitThreads()"

execfile("/home/gnuradio/.grc_gnuradio/IEEE_802_15_4.py")
execfile("/home/gnuradio/.grc_gnuradio/spectrum_decision.py")
execfile("/home/gnuradio/.grc_gnuradio/spectrum_mobility_M.py")
execfile("/home/gnuradio/.grc_gnuradio/spectrum_sensing_M.py")
execfile("/home/gnuradio/.grc_gnuradio/spectrum_sharing_M.py")
execfile("/home/gnuradio/.grc_gnuradio/usrp.py")
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import pmt_cpp
import wx

class master(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="IEEE 802.15.4 Transceiver using OQPSK PHY")

        ##################################################
        # Variables
        ##################################################
        self.gain = gain = 86

        ##################################################
        # Blocks
        ##################################################
        self.usrp_0 = usrp()
        self.spectrum_sharing_M_0 = spectrum_sharing_M()
        self.spectrum_sensing_M_0 = spectrum_sensing_M()
        self.spectrum_mobility_M_0 = spectrum_mobility_M()
        self.spectrum_decision_0 = spectrum_decision()
        self.pmt_cpp_time_transmission_cycle_0 = pmt_cpp.time_transmission_cycle()
        self.pmt_cpp_pmt_extract_master_0 = pmt_cpp.pmt_extract_master()
        self.pmt_cpp_message_generation_0 = pmt_cpp.message_generation()
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        self.IEEE_802_15_4_0 = IEEE_802_15_4()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.IEEE_802_15_4_0, 'rxout'), (self.pmt_cpp_pmt_extract_master_0, 'in_pdu'))    
        self.msg_connect((self.pmt_cpp_message_generation_0, 'msg'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_message_generation_0, 'mp'), (self.usrp_0, 'command_source'))    
        self.msg_connect((self.pmt_cpp_message_generation_0, 'mp'), (self.usrp_0, 'command_sink'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'Ack'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.pmt_cpp_time_transmission_cycle_0, 'in_signal'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.pmt_cpp_time_transmission_cycle_0, 'in_signal'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.spectrum_mobility_M_0, 'flag'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'data'), (self.spectrum_sensing_M_0, 'data_sensing'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.spectrum_sharing_M_0, 'sharing_message'))    
        self.msg_connect((self.pmt_cpp_time_transmission_cycle_0, 'out_signal'), (self.pmt_cpp_message_generation_0, 'signal'))    
        self.msg_connect((self.spectrum_decision_0, 'out'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.spectrum_mobility_M_0, 'signal'), (self.pmt_cpp_message_generation_0, 'signal'))    
        self.msg_connect((self.spectrum_mobility_M_0, 'ccc'), (self.usrp_0, 'command_source'))    
        self.msg_connect((self.spectrum_sensing_M_0, 'ack_repeat'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.spectrum_sensing_M_0, 'ok'), (self.spectrum_decision_0, 'in'))    
        self.msg_connect((self.spectrum_sensing_M_0, 'rna_file'), (self.spectrum_decision_0, 'in'))    
        self.msg_connect((self.spectrum_sensing_M_0, 'tuned'), (self.usrp_0, 'command_source'))    
        self.msg_connect((self.spectrum_sharing_M_0, 'bool'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.spectrum_sharing_M_0, 'new_frequency'), (self.usrp_0, 'command_source'))    
        self.connect((self.IEEE_802_15_4_0, 0), (self.usrp_0, 0))    
        self.connect((self.usrp_0, 0), (self.IEEE_802_15_4_0, 0))    


    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = master()
    tb.Start(True)
    tb.Wait()
