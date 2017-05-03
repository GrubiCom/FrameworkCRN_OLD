/* -*- c++ -*- */
/* 
 * Copyright 2015 Ariel Marques.
 * Universidade Federal de Lavras - UFLA
 * Departamento de Ciencia da Computacao - DCC
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "pmt_extract2_impl.h"
#include "unistd.h"
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <boost/date_time/posix_time/time_parsers.hpp>
#include <boost/date_time/posix_time/time_formatters.hpp>
/*Bloco pmt_extract2
 *Bloco capaz de extrair mensagens de dentro do PDU gerado pelo OOT 802.15.4 
 */

int packet_received = 0;
int sent1=0;
bool sense = false;
bool share = false;
namespace gr {
  namespace pmt_cpp {

    /*Funcao make do pmt_extract2*/
    pmt_extract2::sptr
    pmt_extract2::make()
    {
      return gnuradio::get_initial_sptr
        (new pmt_extract2_impl());
    }

    /*
     * The private constructor
     */
    pmt_extract2_impl::pmt_extract2_impl()
      : gr::block("pmt_extract",
              gr::io_signature::make(0,0,0),
              gr::io_signature::make(0,0,0))
    {
        message_port_register_out(pmt::mp("sense"));     //Registra porta de saida pmt_dict
        message_port_register_out(pmt::mp("share")); 
        message_port_register_out(pmt::mp("Ack"));  
        message_port_register_out(pmt::mp("info_neighbor"));
    	
    	message_port_register_in(pmt::mp("in_pdu"));        //Registra porta de entrada in_pdu
    	set_msg_handler(pmt::mp("in_pdu"), 
                boost::bind(&pmt_extract2_impl::handle_msg, 
                this, _1));                                 //Seta handle_msg em in_pdu
        packet_received = 0;
    }
    pmt_extract2_impl::~pmt_extract2_impl() {

    }

        
        /*
         *Funcao capaz de retirar todo o conteudo desejavel do PDU do 802.15.4
         */
       void
    	pmt_extract2_impl::handle_msg(pmt::pmt_t pdu)
        {
    	//exemplo sense <1:2:2.4:3.9>
           //           
            boost::posix_time::ptime x;           
            //boost::posix_time::ptime tt;
            x = boost::posix_time::microsec_clock::local_time();
           
          // add the field and publish
            pmt::pmt_t meta = pmt::car(pdu);
            pmt::pmt_t vector = pmt::cdr(pdu);
            
            //Testa PDU
            if(pmt::is_null(meta)){
                    meta = pmt::make_dict();
                    } else if(!pmt::is_dict(meta)){
                            throw std::runtime_error("pdu_remove received non PDU input");
            }
            size_t offset(0);
            //Tamanho do PDU
            size_t len = pmt::length(vector);
            std::string lut = "0123456789:.,;-ANT<>";//17 caracteres regex
            int count = 0;
            char str[50];
            //std::cout << "End: " << &str << std::endl;
            const uint8_t* d = (const uint8_t*) pmt::uniform_vector_elements(vector, offset);
            for(size_t i=0; i<len; i+=16){
                    for(size_t j=i; j<std::min(i+16,len); j++){
                            for (size_t x=0; x<20; x++){
                                    if (lut[x] == d[j]) {
                                            str[count] = d[j];
                                            //std::cout<< str[count];
                                            count++;
                                    }
                            }
                    }
                    
            }
            
            //std::cout <<"[SLAVE][MESSAGE PARSER]:Info: "<<str<< std::endl;
            //std::cout <<"[SLAVE][MESSAGE PARSER]:Sense_tag: "<<sense<< std::endl;  
            char idUsrp = '4';
            size_t idMaster = -1;
            char* pEnd;
            double fMax, fMim, nChannel;
            char value[3];
            int pos = 0;
            while(str[pos]!= '<' ){
                pos++;
            }
            //std::cout <<"Info: "<<str<< std::endl;
            if (str[pos] =='<' && (str[pos+1] == idUsrp || str[pos+1] == '0' ) ){ //1
                if (str[pos+1] == '0') {
                    //std::cout <<"[SLAVE][MESSAGE PARSER]:Info: "<<str<< std::endl;
                  // std::cout << "[SLAVE][MESSAGE PARSER]:Broadcast Message" << std::endl;
                }
                
                
                //std::cout <<"Info: "<<str<< std::endl;
                if(str[pos+3] == '0'){//<0:0> Broadcast:ID_MSG
                    std::cout<< "[SLAVE][MESSAGE PARSER]:Discovery of neighbors " << "<N:"<<boost::to_string(idUsrp)<<">"<< std::endl;
                    std::fstream out; 
                    out.open("/tmp/number_packet_received.txt", std::ios::out | std::ios::app);
                    if(out.is_open() && packet_received > 0){
                        out << packet_received << std::endl;
                        std::cout << "[SLAVE][MESSAGE PARSER]:SALVED TOTAL PACKET RECEIVED "<< std::endl;
                        out.close();
                    }
                    packet_received = 0;
                    //message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<N:"+boost::to_string(idUsrp)+">"));
                    srand (time(NULL));
                    int time = std::rand()% 400000 + 100000;
                    //std::cout << "[SLAVE][MESSAGE PARSER]: RAND: "<< time << std::endl;
                    usleep(time);
                    message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<N:"+boost::to_string(idUsrp)+">"));
                   // sense = false;
                }else if (str[pos+3] == '1'){// Comunicação de quem é o master //3
                    std::cout << "[SLAVE][MESSAGE PARSER]:MASTER" << std::endl;
                    idMaster = str[pos+5]; //5
                    
                }else if (str[pos+3] =='2' && !sense){// Comunicação para realizar sense
                    //<1:2:2:3,0>
                    sense = true;
                    share = false;
                    std::cout << "[SLAVE][MESSAGE PARSER]:SENSE" << std::endl;
                    //std::cout << "[SLAVE][MESSAGE PARSER]:"<< "<s:"<<boost::to_string(idUsrp)<<">" << std::endl;
                    message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<s:"+boost::to_string(idUsrp)+">"));//linha nova
                    usleep(1000000);
                    message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<s:"+boost::to_string(idUsrp)+">"));//linha nova
                    remove("/tmp/ack");
                    remove("/tmp/sense.txt");
                    remove("/tmp/send.txt");
                    remove("/tmp/power.txt");
                    remove("/tmp/time.txt");
                    
                    std::string new_str (str);//<1:2:2:3,0>
                    std::size_t p = new_str.find_last_of(":");//<1:2:2(:)3,0>
                    std::string sub_str (new_str.substr(0,p));//<1:2:2
                    std::size_t p1 = sub_str.find_last_of(":");//<1:2(:)2
                    size_t f1 = sub_str.find(",");
                    if (f1 != std::string::npos){
                        sub_str.replace(f1, std::string(",").length(), ".");
                    }
                    std::stringstream sss(sub_str.substr(sub_str.find_last_of(":")+1,p1+1));
                    //std::cout <<"[SLAVE][MESSAGE PARSER]:teste: " <<sss.str()<< " "<<sub_str <<std::endl;
                    /*value[0] = str[pos+5];                    
                    value[1] = ',';
                    value[2] = str[pos+7];
                    if(str[pos+8]!= ':') value[3] = str[pos+8];
                    std::cout <<"[SLAVE][MESSAGE PARSER]:value: " << value[0] << value[1] << value[2] << " atof "<<std::atof(value)<<std::endl;
                    fMim = std::strtod (value,&pEnd); */
                    //sss>> fMim;
                    fMim = std::atof(sss.str().c_str());
                    std::cout << "FMIm: " << fMim << std::endl;
                    fMim *= (double)1.0e9;
                   // std::cout << "[SLAVE][MESSAGE PARSER]: FMIm: " << fMim << std::endl; 
                    pmt::pmt_t p_dict  = pmt::make_dict();
                    p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("mim"), pmt::from_double(fMim));
                    //value[0] = str[pos+9];
                   // value[1] = ',';
                   // value[2] = str[pos+11];
                    
                    std::string st(str); //<1:2:2:3,0>
                    
                    std::size_t pos = st.find_last_of(":");//<1:2:2(:)3,0>
                    std::size_t terminal = st.find_last_of(">");//<1:2:2:3,0(>)
                    //std::cout << "String: " << st << " POS: " << terminal<< std::endl;
                   // std::cout << "SubString: "<< st.substr(pos+1,((terminal)-(pos+1))) << std::endl;
                    std::string su = st.substr(pos+1,((terminal)-(pos+1)));
                    //std::string::size_type sz;
                    size_t f = su.find(",");
                    if (f != std::string::npos){
                        su.replace(f, std::string(",").length(), ".");
                    }
                    std::cout << "SubString:su "<< su << std::endl;
                    std::stringstream ss(su);
                    //ss >> fMax;
                    fMax = std::atof(ss.str().c_str());
                    //fMax = std::strtod(st.substr(pos+1,terminal).c_str(),&pEnd);
                    std::cout <<"[SLAVE][MESSAGE PARSER]:value: " << ss.str()<<std::endl;
                    //fMax = std::strtod (value,&pEnd); 
                    //str = NULL; std::free(str);
                    fMax *= 1e9;     
                    std::cout << "[SLAVE][MESSAGE PARSER]: FMax: " << fMax << std::endl;
                    p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("max"), pmt::from_double(fMax));
                    p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("sense"), pmt::PMT_T);
                    
                    message_port_pub(pmt::mp("sense"), p_dict);                    
                }else if (str[pos+3] =='3' && !share){// Comunicação de novo canal
                    //<1:3:2,4>
                    sense = false;
                    
                    std::cout << "[SLAVE][MESSAGE PARSER]:SHARE" << std::endl;
                    
                    std::string st(str); 
                    std::size_t pos = st.find_last_of(":");
                    std::size_t terminal = st.find_last_of(">");
                    //std::cout << "String: " << st << " POS: " << pos<< std::endl;
                    //std::cout << "SubString: "<< st.substr(pos+1,terminal) << std::endl;
                    //std::string::size_type sz;
                    size_t f = st.find(".");
                    if (f != std::string::npos){
                        st.replace(f, std::string(".").length(), ",");
                    }
                    nChannel = std::strtod(st.substr(pos+1,terminal).c_str(),&pEnd);
                    std::cout << "[SLAVE][MESSAGE PARSER]:nChannel: " << nChannel<< std::endl;
                    //std::free(str);
                    //nChannel = std::strtod (value,&pEnd); 
                    
                    message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<0:3:"+boost::to_string(nChannel)+">"));
                    nChannel *= 1e9;
                    //std::ofstream micro;
                    //micro.open("/tmp/total_microseconds.txt",  std::ios::app);
                    //micro << nChannel<< std::endl;
                    //micro.close();
                    pmt::pmt_t p_dict  = pmt::make_dict();
                    p_dict = pmt::dict_add(p_dict, pmt::string_to_symbol("nChannel"), pmt::from_double(nChannel));
                    share = true;
                    message_port_pub(pmt::mp("share"), p_dict);
                } else if (str[pos+1] == idUsrp && str[pos+3] == '5' ){
                    sense = false;
                    share = false;
                    boost::posix_time::ptime t,t2;            
                    //boost::posix_time::ptime tt;
                    t = boost::posix_time::microsec_clock::local_time();
                    
                    /*Fazendo a porra do ack de merda
                     */
                    
                    
                    std::cout << "[SLAVE][MASSAGE PARSER]: RECEIVED PACKET DATA TRANSMISSION " <<packet_received << std::endl;
                    //std::cout << "MSG: "<< str << std::endl;
                    std::string st(str);
                    std::size_t po = st.find(":",7);
                    //std::cout << " st " << st<< std::endl;
                    
                    std::string cu = st.substr(7,po-7);
                    std::ofstream arq;
                    arq.open("/tmp/time.txt",  std::ios::app);
                    arq << cu<< std::endl;
                    arq.close();
                    std::size_t p = st.find_last_of(":");
                    std::size_t terminal = st.find(">");
                    std::string sub = st.substr(p+1,terminal-(p+1));
                    //std::cout << " sub " << sub<< std::endl;
                    //std::cout << "time: "<< boost::posix_time::to_iso_string(t) << std::endl;
                    try{
                        t2 = boost::posix_time::from_iso_string(sub);
                        boost::posix_time::time_duration t1 = t - t2;
                       // std::cout << t1.fractional_seconds() << std::endl;
                        //std::cout << t1.ticks_per_second() << std::endl;
                        //std::cout << t1.total_microseconds() << std::endl;
                        //std::cout << t1.total_nanoseconds() << std::endl;
                        std::ofstream micro;
                        micro.open("/tmp/total_microseconds.txt",  std::ios::app);
                        micro << t1.total_microseconds()<< std::endl;
                        micro.close(); 
                    }catch (...){
                        //std::cout << "Date error" << std::endl;
                    }
                    
                    
                    //packet_received++;
                }else if (str[pos+1] == idUsrp && str[pos+3] == '4' ) {
                    //std::cout << "[MASTER][MESSAGE PARSER]: DATA "<< std::endl;

                    std::string st(str); 
                    std::size_t po = st.find(":",7);
                    std::string su = st.substr(7,po-7);
                    std::size_t terminal = st.find(">");
                    std::size_t p = st.find_last_of(":",terminal-1);
                    //std::cout << "[SLAVE][MASSAGE PARSER]: RECEIVED PACKET DATA TRANSMISSION " <<received << std::endl;
                    packet_received++;

                    //cochar id = str[pos+5];
                    std::string filename = "/tmp/";

                    filename.append("received_pack");
                    filename.push_back(str[pos+5]);
                    filename.append(".txt");
                   // std::remove(filename.c_str());
                    std::fstream arq;
                    //arq.open(filename.c_str(), std::ios::out | std::ios::app);
                    ////arq << received<< std::endl;
                    //arq.close();
                    std::string sub = st.substr(p+1,terminal-(p+1));



                    std::string str2(str);
                    str2[pos+1] = str[pos+5];
                    str2[pos+5] = str[pos+1];
                    //std::cout << "terminal: " << terminal << std::endl;
                    std::cout << "<"<<str[pos+5]<<":4:"<<"0:"<< su<<":00011110000000000000000000000000000000000000000000000:"<<sub<<">"<<std::endl;
                    //usleep(10000);
                    //t2 = boost::posix_time::microsec_clock::local_time();
                    /*boost::posix_time::time_duration t1 = t2 - t;
                            std::cout << t1.fractional_seconds() << std::endl;
                            std::cout << t1.ticks_per_second() << std::endl;
                            std::cout << t1.total_microseconds() << std::endl;
                            std::cout << t1.total_nanoseconds() << std::endl;*/
                    if((int)packet_received % 53 == 0){
                        message_port_pub(pmt::mp("info_neighbor"), pmt::intern("<"+boost::to_string(str[pos+5])+":5:"+idUsrp+":"+su+":00011110000000000000000000000000000000000000000000000:"+sub+">"));
                    
                    }//message_port_pub(pmt::mp("Ack"), pmt::intern(boost::to_string(str2)));
                    //std::cout << "SUB: " << sub << std::endl;
                    std::string filename1 = "/tmp/";
                    sent1++;
                    filename1.append("sent_pack");
                    filename1.push_back(str[pos+5]);
                    filename1.append(".txt");
                    //std::remove(filename1.c_str());
                    std::fstream se;
                    se.open(filename1.c_str(), std::ios::out | std::ios::app);
                    se << sent1<< std::endl;
                    se.close();
                }
            }else if(str[pos] =='<' && str[pos+1] == 'A' && str[pos+3] == idUsrp){
               // sense = false;
                //std::cout << "ACK" << std::endl;
                //int a = str[pos+5] - '0';
                std::string st(str); 
                //std::free(str);
                std::size_t pos = st.find_last_of(":");
                std::size_t terminal = st.find_last_of(">");
                //std::cout << "[SLAVE][MESSAGE PARSER]: String: " << st << " POS: " << pos<< std::endl;
               // std::cout << "[SLAVE][MESSAGE PARSER]: SubString: "<< st.substr(pos+1,terminal) << std::endl;
                std::string::size_type sz;
                int bla = std::atoi(st.substr(pos+1,terminal).c_str());
                //std::cout << "[SLAVE][MESSAGE PARSER]: Bla: " << bla<< std::endl;
                int a = bla;
                if (a == 1){// Salva a primeira mensagem recebida
                    std::fstream out;
                    out.open("/tmp/ack.txt", std::ios::out);
                    if(out.is_open()){
                        out << a;
                        std::cout << "[SLAVE][MESSAGE PARSER]:SALVANDO "<< a <<std::endl;
                    }else{
                        std::cerr << "file ~/ack.txt don't exist" << std::endl;
                        std::exit(-1);
                    }
                    out.close();
                }
                pmt::pmt_t dict  = pmt::make_dict();
                dict = pmt::dict_add(dict, pmt::string_to_symbol("ack"), pmt::from_long(a));
                std::cout << "[SLAVE][MESSAGE PARSER]: ACK" << std::endl;
                //sleep(1);
                message_port_pub(pmt::mp("Ack"), dict);
                sense = false;
                share = false;
            }else if(str[pos+1] == 'N'){
                //sense = false;
                //Descobertas dos vizinhos<N:ID_neighbor>
                //std::cout<< "VIZINHOS" << std::endl;
                std::fstream file1;
                std::string filename = "/tmp/neighbors_slave.txt";
                std::string neighbor_f;
                std::ifstream file; // open file
                file.open(filename.c_str());
                std::string id_neighbor = boost::to_string(str[pos+3]);
                bool contained = false;
                if(file.is_open()){
                    while(getline(file,neighbor_f)){
                        //std::cout<< "VIZINHOS1" << std::endl;

                        if(neighbor_f.compare(id_neighbor) == 0 ){
                            contained = true;
                        }
                    }
                    file.close();
                    
                }
                if(!contained  && (id_neighbor.compare(boost::to_string(idUsrp))!= 0)){
                   // std::cout<< "VIZINHOS2" << std::endl;
                    std::cout << "[SLAVE][MESSAGE PARSER]: Saved "<<str << std::endl;
                    file1.open(filename.c_str(), std::ios::in | std::ios::out | std::ios::app); 
                    if(file1.is_open()){
                        file1 << id_neighbor<< std::endl;
                        file1.close();
                    }
                }       
                
            }else if (str[pos+1] != idUsrp && str[pos+1] != '0'){
                //str = NULL; std::free(str);
                //std::cout << "[SLAVE][MESSAGE PARSER]: Pacote nao destinado a usrp de ID: "<<idUsrp << std::endl;                  
            }else{
                //str = NULL; std::free(str);
                std::cout << "[SLAVE][MESSAGE PARSER]: Lixo" << std::endl;
            }
            for (int i = 0; i < 50; i++) str[i] = 0;
            //sense=false;
        }
       

  } /* namespace pmt_cpp */
} /* namespace gr */

