#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Cognitive network over IEEE 802.15.4
# Author: Ariel Marques
# Generated: Fri Mar 25 13:25:18 2016
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

execfile("/home/vanet2/.grc_gnuradio/File_Recorder.py")
execfile("/home/vanet2/.grc_gnuradio/Get_Power.py")
execfile("/home/vanet2/.grc_gnuradio/IEEE_802_15_4.py")
from gnuradio import blocks
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

class Cog_sense(grc_wxgui.top_block_gui):

    def __init__(self, samp_rate=4e6):
        grc_wxgui.top_block_gui.__init__(self, title="Cognitive network over IEEE 802.15.4")

        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.gain = gain = 89
        self.bw = bw = 1000e3

        ##################################################
        # Blocks
        ##################################################
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label="79",
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
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(6000000000, 0)
        self.uhd_usrp_source_0.set_gain(30, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(bw, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(6000000000, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(bw, 0)
        self.pmt_cpp_wait_first_ack_0 = pmt_cpp.wait_first_ack()
        self.pmt_cpp_transmission_data_0 = pmt_cpp.transmission_data()
        self.pmt_cpp_start_share_0 = pmt_cpp.start_share()
        self.pmt_cpp_start_sense_0 = pmt_cpp.start_sense()
        self.pmt_cpp_set_ccc_0 = pmt_cpp.set_ccc()
        self.pmt_cpp_send_file_ACK_2 = pmt_cpp.send_file_ACK()
        self.pmt_cpp_pmt_extract2_0 = pmt_cpp.pmt_extract2()
        self.pmt_cpp_file_connect_0 = pmt_cpp.file_connect()
        self.pmt_cpp_ACK_0 = pmt_cpp.ACK()
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.IEEE_802_15_4_0 = IEEE_802_15_4()
        self.Get_Power_0 = Get_Power()
        self.File_Recorder_0 = File_Recorder()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.File_Recorder_0, 'file_ready'), (self.pmt_cpp_send_file_ACK_2, 'file_ready'))    
        self.msg_connect((self.IEEE_802_15_4_0, 'rxout'), (self.pmt_cpp_pmt_extract2_0, 'in_pdu'))    
        self.msg_connect((self.pmt_cpp_ACK_0, 'msg'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_ACK_0, 'first'), (self.pmt_cpp_wait_first_ack_0, 'fisrt_message'))    
        self.msg_connect((self.pmt_cpp_file_connect_0, 'bool'), (self.File_Recorder_0, 'in_pdu'))    
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'info_neighbor'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'Ack'), (self.pmt_cpp_ACK_0, 'Ack'))    
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'sense'), (self.pmt_cpp_start_sense_0, 'pmt::dict'))    
        self.msg_connect((self.pmt_cpp_pmt_extract2_0, 'share'), (self.pmt_cpp_start_share_0, 'pmt::dict'))    
        self.msg_connect((self.pmt_cpp_send_file_ACK_2, 'pdu'), (self.pmt_cpp_ACK_0, 'File_Ready'))    
        self.msg_connect((self.pmt_cpp_set_ccc_0, 'ccc'), (self.uhd_usrp_sink_0, 'command'))    
        self.msg_connect((self.pmt_cpp_set_ccc_0, 'ccc'), (self.uhd_usrp_source_0, 'command'))    
        self.msg_connect((self.pmt_cpp_start_sense_0, 'bool'), (self.File_Recorder_0, 'bool'))    
        self.msg_connect((self.pmt_cpp_start_sense_0, 'bool'), (self.pmt_cpp_file_connect_0, 'in_pdu'))    
        self.msg_connect((self.pmt_cpp_start_sense_0, 'pmt::mp'), (self.uhd_usrp_sink_0, 'command'))    
        self.msg_connect((self.pmt_cpp_start_sense_0, 'pmt::mp'), (self.uhd_usrp_source_0, 'command'))    
        self.msg_connect((self.pmt_cpp_start_share_0, 'bool'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_start_share_0, 'bool'), (self.pmt_cpp_set_ccc_0, 'flag'))    
        self.msg_connect((self.pmt_cpp_start_share_0, 'bool'), (self.pmt_cpp_transmission_data_0, 'signal_in'))    
        self.msg_connect((self.pmt_cpp_start_share_0, 'pmt::mp'), (self.uhd_usrp_sink_0, 'command'))    
        self.msg_connect((self.pmt_cpp_start_share_0, 'pmt::mp'), (self.uhd_usrp_source_0, 'command'))    
        self.msg_connect((self.pmt_cpp_transmission_data_0, 'signal_out'), (self.Get_Power_0, 'in_pdu'))    
        self.msg_connect((self.pmt_cpp_transmission_data_0, 'packet'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.pmt_cpp_wait_first_ack_0, 'message_repeat'), (self.IEEE_802_15_4_0, 'msg'))    
        self.connect((self.IEEE_802_15_4_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.pmt_cpp_file_connect_0, 0), (self.File_Recorder_0, 0))    
        self.connect((self.pmt_cpp_file_connect_0, 1), (self.blocks_null_sink_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.Get_Power_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.IEEE_802_15_4_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.pmt_cpp_file_connect_0, 0))    


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.uhd_usrp_sink_0.set_bandwidth(self.bw, 0)
        self.uhd_usrp_source_0.set_bandwidth(self.bw, 0)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(4e6),
        help="Set samp_rate [default=%default]")
    (options, args) = parser.parse_args()
    tb = Cog_sense(samp_rate=options.samp_rate)
    tb.Start(True)
    tb.Wait()
