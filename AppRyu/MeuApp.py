from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
#Pacotes
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp
from ryu.lib.packet import tcp
from ryu.lib.packet import udp
from ryu.lib.packet import igmp
#Extras
from ryu.lib.dpid import dpid_to_str
from ryu.ofproto.ofproto_v1_2 import OFPG_ANY
from ryu.lib.mac import haddr_to_bin
#Topologia
from ryu.topology import event, switches
from ryu.topology.api import get_switch, get_link
import networkx as nx
#Sistema
import os
import requests
import pickle
#from classe import Classe

class trabalho(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(trabalho, self).__init__(*args, **kwargs)
    #Packet In
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        #Tipos de pacotes
        pkt_ethernet = pkt.get_protocol(ethernet.ethernet)
        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_icmp = pkt.get_protocol(icmp.icmp)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        pkt_udp = pkt.get_protocol(udp.udp)
        pkt_igmp = pkt.get_protocol(igmp.igmp)

        if pkt_igmp:
            print('Pacote IGMP!!')
            print(dir(pkt_igmp.parser))
            print(pkt_igmp.records)
            print(pkt_igmp.get_packet_type)
            print(dir(pkt_igmp))
            print(pkt_igmp.stringify_attrs)






#Tudo o que eu quiser iniciar, basta colocar aqui!!
#Require
#app_manager.require_app('ryu.app.ofctl_rest')
app_manager.require_app('ryu.app.simple_switch_13_mod')
#app_manager.require_app('ryu.app.simple_switch_13')
#app_manager.require_app('ryu.app.rest_conf_switch')
#app_manager.require_app('ryu.app.rest_topology')
#app_manager.require_app('ryu.app.rest_qos_mod')
