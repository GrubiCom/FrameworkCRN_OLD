#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: IEEE 802.15.4 Transceiver using OQPSK PHY
# Generated: Thu Mar 30 12:29:20 2017
##################################################

# Call XInitThreads as the _very_ first thing.
# After some Qt import, it's too late

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
from optparse import OptionParser
import pmt_cpp

class master(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "IEEE 802.15.4 Transceiver using OQPSK PHY")

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


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = master()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
