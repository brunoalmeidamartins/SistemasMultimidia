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
from ryu.lib import igmplib
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
import time
#from classe import Classe

#Variaveis Globais
#Lista IPs que serviram de Multicast
LISTA_MULTICAST_IPS_SERVICOS = {'10.0.0.20':'ff:ff:ff:00:20:00',
                                '10.0.0.21':'ff:ff:ff:00:21:00',
                                '10.0.0.22':'ff:ff:ff:00:20:00',
                                '10.0.0.23':'ff:ff:ff:00:20:00',
                                '10.0.0.24':'ff:ff:ff:00:20:00',
                                '10.0.0.25':'ff:ff:ff:00:20:00',
}




path_home = os.getenv("HOME") #Captura o caminho da pasta HOME
#Switches e seus Hosts
S1 = ['10.0.0.1','10.0.0.2','10.0.0.3']
S2 = []
S3 = ['10.0.0.8','10.0.0.9']
S4 = ['10.0.0.4','10.0.0.5']
S5 = ['10.0.0.6','10.0.0.7']
LISTA_SWITCHES = [S1,S2,S3,S4,S5]
#Grafo da Rede

GRAFO = nx.MultiGraph()
GRAFO.add_edge('10.0.0.1','S1',cost=1,index=0)
GRAFO.add_edge('10.0.0.2','S1',cost=1,index=1)
GRAFO.add_edge('10.0.0.3','S1',cost=1,index=2)
GRAFO.add_edge('10.0.0.4','S4',cost=1,index=3)
GRAFO.add_edge('10.0.0.5','S4',cost=1,index=4)
GRAFO.add_edge('10.0.0.6','S5',cost=1,index=5)
GRAFO.add_edge('10.0.0.7','S5',cost=1,index=6)
GRAFO.add_edge('10.0.0.8','S3',cost=1,index=7)
GRAFO.add_edge('10.0.0.9','S3',cost=1,index=8)
GRAFO.add_edge('S1','S2',cost=1,index=9)
GRAFO.add_edge('S3','S2',cost=1,index=10)
GRAFO.add_edge('S4','S2',cost=1,index=11)
GRAFO.add_edge('S5','S2',cost=1,index=12)

#MAC do Controlador
MAC_CONTROLADOR = 'ff:ff:ff:00:00:00'
#IP do controlador
IP_CONTROLADOR = '10.0.0.99'
#Porta de envio Servicos Multicast
PORTA_MULTICAST = 27000
#Porta para dizer a oferta de Servicos
PORTA_OFERTA_SERVICO = 23000
#Lista de grupos Multicast
LISTA_GRUPO_MULTICAST = []
#Fim Variaveis Globais


class trabalho(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(trabalho, self).__init__(*args, **kwargs)

    #This function gets triggered before the topology controller flows are added
    #But late enough to be able to remove flows
    @set_ev_cls(ofp_event.EventOFPStateChange, [CONFIG_DISPATCHER])
    def state_change_handler(self, ev):
        dp = ev.datapath
        ofp = dp.ofproto
        parser = dp.ofproto_parser

        #Delete any possible currently existing flows.
        del_flows = parser.OFPFlowMod(dp, table_id=ofp.OFPTT_ALL, out_port=ofp.OFPP_ANY, out_group=ofp.OFPG_ANY, command=ofp.OFPFC_DELETE)
        dp.send_msg(del_flows)

        #Delete any possible currently exising groups
        del_groups = parser.OFPGroupMod(datapath=dp, command=ofp.OFPGC_DELETE, group_id=ofp.OFPG_ALL)
        dp.send_msg(del_groups)

        #Make sure deletion is finished using a barrier before additional flows are added
        barrier_req = parser.OFPBarrierRequest(dp)
        dp.send_msg(barrier_req)

    '''
    Instala regras na inicializacao
    '''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        '''
        Envia Regra de Packet_In para os switches
        '''
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        actions = [parser.OFPActionOutput(port=ofproto.OFPP_CONTROLLER,
                                          max_len=ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(type_=ofproto.OFPIT_APPLY_ACTIONS,
                                             actions=actions)]
        #match = parser.OFPMatch()
        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=0,
                                match=parser.OFPMatch(),
                                instructions=inst)
        datapath.send_msg(mod)
        #print(mod)
        '''
        Fim Regra de Packet_In para os switches
        '''
        try:
            '''
            Regra de Packet In para Servico Multicast
            '''
            id_switch = datapath.id
            os.system('ovs-ofctl add-flow s' + str(id_switch) + ' priority=40000,dl_type=0x0800,nw_proto=17,tp_dst='+str(PORTA_OFERTA_SERVICO)+',actions=output:controller') #Envia o servico Multicast
            #os.system('ovs-ofctl add-flow s' + str(id_switch) + ' priority=40000,dl_type=0x0800,nw_proto=17,tp_dst='+str(PORTA_MULTICAST)+',actions=output:controller') #Envia o Fluxo Multicast
            '''
            Fim Regra de Packet In para Servico Multicast
            '''
        except Exception as e:
            print(e)
    #igmp
    @set_ev_cls(igmplib.EventMulticastGroupStateChanged,
                MAIN_DISPATCHER)
    def _status_changed(self, ev):
        msg = {
            igmplib.MG_GROUP_ADDED: 'Multicast Group Added',
            igmplib.MG_MEMBER_CHANGED: 'Multicast Group Member Changed',
            igmplib.MG_GROUP_REMOVED: 'Multicast Group Removed',
        }
        self.logger.info("%s: [%s] querier:[%s] hosts:%s",
                         msg.get(ev.reason), ev.address, ev.src,
                         ev.dsts)

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

        #Responde o ARP com pedido de MAC do controlador
        if pkt_arp:
            if str(pkt_arp.dst_ip) == IP_CONTROLADOR: #Envia ARP response com o MAC do controlador
                if pkt_arp.opcode == arp.ARP_REQUEST:
                    port1 = msg.match['in_port']
                    pkt = packet.Packet()
                    pkt.add_protocol(ethernet.ethernet(ethertype=pkt_ethernet.ethertype,
                                                       dst=pkt_ethernet.src,
                                                       src=MAC_CONTROLADOR))
                    pkt.add_protocol(arp.arp(opcode=arp.ARP_REPLY,
                                             src_mac=MAC_CONTROLADOR,
                                             src_ip=IP_CONTROLADOR,
                                             dst_mac=pkt_arp.src_mac,
                                             dst_ip=pkt_arp.src_ip))
                    self._send_packet(datapath, port1, pkt)
                    #print("ARP Respondido!!")
            else:
                if str(pkt_arp.dst_ip) in LISTA_MULTICAST_IPS_SERVICOS:
                    if pkt_arp.opcode == arp.ARP_REQUEST:
                        port1 = msg.match['in_port']
                        pkt = packet.Packet()
                        pkt.add_protocol(ethernet.ethernet(ethertype=pkt_ethernet.ethertype,
                                                           dst=pkt_ethernet.src,
                                                           src=LISTA_MULTICAST_IPS_SERVICOS[str(pkt_arp.dst_ip)]))
                        pkt.add_protocol(arp.arp(opcode=arp.ARP_REPLY,
                                                 src_mac=LISTA_MULTICAST_IPS_SERVICOS[str(pkt_arp.dst_ip)],
                                                 src_ip=str(pkt_arp.dst_ip),
                                                 dst_mac=pkt_arp.src_mac,
                                                 dst_ip=pkt_arp.src_ip))
                        self._send_packet(datapath, port1, pkt)


        #Verifica se o pacote UDP foi gerado na porta de oferta de servico
        if pkt_udp:
            if pkt_udp.dst_port == PORTA_OFERTA_SERVICO:
                if pkt_ipv4.dst == IP_CONTROLADOR:
                    #Responde o pacote
                    pkt2 = pkt.get_protocol(ethernet.ethernet)
                    port1 = msg.match['in_port']
                    pkt_resp = packet.Packet()
                    e = ethernet.ethernet(ethertype=pkt2.ethertype,dst=pkt_ethernet.src,src=MAC_CONTROLADOR) #Parte da camada Rede
                    i = ipv4.ipv4(dst=pkt_ipv4.src,src=IP_CONTROLADOR,proto=17) #Parte do IP
                    u = udp.udp(dst_port=pkt_udp.src_port,src_port=1234) #Parte do UDP
                    pkt_resp = e/i/u #Monta o pacote
                    self._send_packet(datapath, port1, pkt_resp)
                    #Guarda o servico a ser oferta na lista
                    time.sleep(1)
                    global LISTA_GRUPO_MULTICAST
                    arq = open(path_home+'/SistemasMultimidia/AppRyu/ip_servico_multicast.txt','r')
                    ip_multicast = arq.read()
                    if ip_multicast not in LISTA_GRUPO_MULTICAST:
                        print("Lista de Grupos Multicast existentes!!")
                        LISTA_GRUPO_MULTICAST.append(ip_multicast)
                        print(LISTA_GRUPO_MULTICAST)
                        #Regra para dropar os pacotes no Swtich ate que tenha clientes
                        switch_onde_esta_ip = self.retornaSwitchIP(str(pkt_ipv4.src))
                        os.system('ovs-ofctl add-flow ' + switch_onde_esta_ip + ' priority=45000,dl_type=0x0800,nw_proto=17,nw_src='+str(pkt_ipv4.src)+',nw_dst='+ip_multicast+',tp_dst='+str(PORTA_MULTICAST)+',actions=drop')
                        print("Regra de DROP APLICADA!!!")


        if pkt_igmp:
            print('Pacote IGMP!!')
            print(pkt_igmp)
            print(pkt_igmp.records)
            for i in pkt_igmp.records:
                #print(dir(i))
                print(i.address)
                print(i.num)
            print('Pacote IPV4')
            print(pkt_ipv4)
            print(pkt_ipv4.src)
            print(datapath.id)

            #print(dir(pkt_igmp.parser))
            #print(pkt_igmp.records)
            #print(pkt_igmp.get_packet_type)
            #print(dir(pkt_igmp))
            #print(pkt_igmp.stringify_attrs)

    '''
    Envia Pacote para Host
    '''
    def _send_packet(self, datapath, port, pkt):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        pkt.serialize()
        #self.logger.info("packet-out %s" % (pkt,))
        data = pkt.data
        actions = [parser.OFPActionOutput(port=port)]
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=ofproto.OFP_NO_BUFFER,
                                  in_port=ofproto.OFPP_CONTROLLER,
                                  actions=actions,
                                  data=data)
        datapath.send_msg(out)
    '''
    FIM Envia Pacote para Host
    '''
    '''
    Encontra o switch onde esta o ip
    '''
    def retornaSwitchIP(self,ip):
        index = -1
        switch = ''
        for i in range(len(LISTA_SWITCHES)):
            if ip in LISTA_SWITCHES[i]:
                index = i+1
        if index == 1:
            switch = 's1'
        elif index == 2:
            switch = 's2'
        elif index == 3:
            switch = 's3'
        elif index == 4:
            switch = 's4'
        elif index == 5:
            switch = 's5'
        else:
            switch = 'Erro'
        return switch
    '''
    FIM Encontra o switch onde esta o ip
    '''

#Tudo o que eu quiser iniciar, basta colocar aqui!!
#Require
#app_manager.require_app('ryu.app.ofctl_rest')
app_manager.require_app('ryu.app.simple_switch_13_modTrabalhoMultimidia')
#app_manager.require_app('ryu.app.simple_switch_igmp_13')
#app_manager.require_app('ryu.app.rest_conf_switch')
#app_manager.require_app('ryu.app.rest_topology')
#app_manager.require_app('ryu.app.rest_qos_mod')
