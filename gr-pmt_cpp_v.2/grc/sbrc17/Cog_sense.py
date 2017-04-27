#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph f
# Title: Cognitive network over IEEE 802.15.4
# Generated: Thu Mar 30 12:36:54 2017
##################################################

# Call XInitThreads as the _very_ first thing.
# After some Qt import, it's too late

execfile("/home/gnuradio/.grc_gnuradio/IEEE_802_15_4.py")
execfile("/home/gnuradio/.grc_gnuradio/send_data_sense.py")
execfile("/home/gnuradio/.grc_gnuradio/spectrum_mobility.py")
execfile("/home/gnuradio/.grc_gnuradio/spectrum_sensing.py")
execfile("/home/gnuradio/.grc_gnuradio/spectrum_sharing.py")
execfile("/home/gnuradio/.grc_gnuradio/usrp.py")
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt_cpp

class Cog_sense(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Cognitive network over IEEE 802.15.4")

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
        self.spectrum_mobility_0 = spectrum_mobility()
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
        self.msg_connect((self.pmt_cpp_transmission_data_0, 'signal_out'), (self.spectrum_mobility_0, 'signal'))    
        self.msg_connect((self.send_data_sense_0, 'message'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.send_data_sense_0, 'repeat_message'), (self.IEEE_802_15_4_0, 'msg'))    
        self.msg_connect((self.spectrum_mobility_0, 'ccc'), (self.usrp_0, 'command_source'))    
        self.msg_connect((self.spectrum_sensing_0, 'file_ready'), (self.send_data_sense_0, 'file_ready'))    
        self.msg_connect((self.spectrum_sensing_0, 'sense_tune_command'), (self.usrp_0, 'command_source'))    
        self.msg_connect((self.spectrum_sharing_0, 'bool'), (self.pmt_cpp_transmission_data_0, 'signal_in'))    
        self.msg_connect((self.spectrum_sharing_0, 'bool'), (self.spectrum_mobility_0, 'flag'))    
        self.msg_connect((self.spectrum_sharing_0, 'new_freq'), (self.usrp_0, 'command_sink'))    
        self.connect((self.IEEE_802_15_4_0, 0), (self.usrp_0, 0))    
        self.connect((self.usrp_0, 0), (self.IEEE_802_15_4_0, 0))    
        self.connect((self.usrp_0, 0), (self.spectrum_mobility_0, 0))    
        self.connect((self.usrp_0, 0), (self.spectrum_sensing_0, 0))    


    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = Cog_sense()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
