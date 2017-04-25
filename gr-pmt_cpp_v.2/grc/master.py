#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver using OQPSK PHY
# Generated: Tue Apr 25 16:59:04 2017
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

execfile("/home/vanet2/.grc_gnuradio/IEEE_802_15_4.py")
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import pmt_cpp
import time
import wx

class master(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="IEEE 802.15.4 Transceiver using OQPSK PHY")

        ##################################################
        # Variables
        ##################################################
        self.gain = gain = 89

        ##################################################
        # Blocks
        ##################################################
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
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(4000000)
        self.uhd_usrp_source_0.set_center_freq(6000000000, 0)
        self.uhd_usrp_source_0.set_gain(40, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(1000e3, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(4000000)
        self.uhd_usrp_sink_0.set_center_freq(6000000000, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(1000e3, 0)
        self.pmt_cpp_timer_0 = pmt_cpp.timer()
        self.pmt_cpp_time_transmission_cycle_0 = pmt_cpp.time_transmission_cycle()
        self.pmt_cpp_time_0 = pmt_cpp.time()
        self.pmt_cpp_set_new_config_master_0 = pmt_cpp.set_new_config_master()
        self.pmt_cpp_set_ccc_master_0 = pmt_cpp.set_ccc_master()
        self.pmt_cpp_preprocessor_master_0 = pmt_cpp.preprocessor_master()
        self.pmt_cpp_pmt_extract_master_0 = pmt_cpp.pmt_extract_master()
        self.pmt_cpp_message_generation_0 = pmt_cpp.message_generation()
        self.pmt_cpp_data_extract_master_0 = pmt_cpp.data_extract_master("/tmp/res_sense.txt")
        self.pmt_cpp_cogmac_0 = pmt_cpp.cogmac()
        self.IEEE_802_15_4_0 = IEEE_802_15_4()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.IEEE_802_15_4_0, 'rxout'), (self.pmt_cpp_pmt_extract_master_0, 'in_pdu'))    
        self.msg_connect((self.pmt_cpp_cogmac_0, 'out'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_message_generation_0, 'msg'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_message_generation_0, 'mp'), (self.uhd_usrp_sink_0, 'command'))    
        self.msg_connect((self.pmt_cpp_message_generation_0, 'mp'), (self.uhd_usrp_source_0, 'command'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'Ack'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'data'), (self.pmt_cpp_data_extract_master_0, 'pdus'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.pmt_cpp_set_ccc_master_0, 'flag'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.pmt_cpp_set_ccc_master_0, 'flag'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.pmt_cpp_set_new_config_master_0, 'pmt::dict'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'data'), (self.pmt_cpp_time_0, 'Ack'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'share'), (self.pmt_cpp_time_transmission_cycle_0, 'in_signal'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.pmt_cpp_time_transmission_cycle_0, 'in_signal'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.uhd_usrp_sink_0, 'command'))    
        self.msg_connect((self.pmt_cpp_pmt_extract_master_0, 'freq'), (self.uhd_usrp_source_0, 'command'))    
        self.msg_connect((self.pmt_cpp_preprocessor_master_0, 'rna_file'), (self.pmt_cpp_cogmac_0, 'in'))    
        self.msg_connect((self.pmt_cpp_preprocessor_master_0, 'rna_file'), (self.pmt_cpp_timer_0, 'in2'))    
        self.msg_connect((self.pmt_cpp_preprocessor_master_0, 'tuned'), (self.uhd_usrp_sink_0, 'command'))    
        self.msg_connect((self.pmt_cpp_preprocessor_master_0, 'tuned'), (self.uhd_usrp_source_0, 'command'))    
        self.msg_connect((self.pmt_cpp_set_ccc_master_0, 'signal'), (self.pmt_cpp_message_generation_0, 'signal'))    
        self.msg_connect((self.pmt_cpp_set_ccc_master_0, 'ccc'), (self.uhd_usrp_sink_0, 'command'))    
        self.msg_connect((self.pmt_cpp_set_ccc_master_0, 'ccc'), (self.uhd_usrp_source_0, 'command'))    
        self.msg_connect((self.pmt_cpp_set_new_config_master_0, 'bool'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_set_new_config_master_0, 'pmt::mp'), (self.uhd_usrp_sink_0, 'command'))    
        self.msg_connect((self.pmt_cpp_set_new_config_master_0, 'pmt::mp'), (self.uhd_usrp_source_0, 'command'))    
        self.msg_connect((self.pmt_cpp_time_0, 'Ack_repeat'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_time_0, 'id_neighbor'), (self.pmt_cpp_preprocessor_master_0, 'id_neighbor'))    
        self.msg_connect((self.pmt_cpp_time_0, 'Feed_back'), (self.pmt_cpp_time_0, 'Ack'))    
        self.msg_connect((self.pmt_cpp_time_0, 'id_neighbor'), (self.pmt_cpp_timer_0, 'in'))    
        self.msg_connect((self.pmt_cpp_time_transmission_cycle_0, 'out_signal'), (self.pmt_cpp_message_generation_0, 'signal'))    
        self.msg_connect((self.pmt_cpp_time_transmission_cycle_0, 'out_signal'), (self.pmt_cpp_set_ccc_master_0, 'flag'))    
        self.msg_connect((self.pmt_cpp_timer_0, 'out'), (self.pmt_cpp_cogmac_0, 'in'))    
        self.connect((self.IEEE_802_15_4_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.IEEE_802_15_4_0, 0))    


    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    tb = master()
    tb.Start(True)
    tb.Wait()
