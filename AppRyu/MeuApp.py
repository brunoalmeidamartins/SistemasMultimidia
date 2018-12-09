from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
#from ryu.ofproto import ofproto_v1_0
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
from ryu.lib.dpid import str_to_dpid
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
#Mapeamento estatico de IPs_Porta
SWITCH_S1 = {'10.0.0.1':1,'10.0.0.2':2,'10.0.0.3':3} #Qualquer outro sai na porta 5
SWITCH_S2 = {'10.0.0.1':1,'10.0.0.2':1,'10.0.0.3':1,'10.0.0.4':3,'10.0.0.5':3,'10.0.0.6':4,'10.0.0.7':4,'10.0.0.8':2,'10.0.0.9':2}
SWITCH_S3 = {'10.0.0.8':1,'10.0.0.9':2} #Qualquer outro sai na porta 5
SWITCH_S4 = {'10.0.0.4':1,'10.0.0.5':2} #Qualquer outro sai na porta 5
SWITCH_S5 = {'10.0.0.6':1,'10.0.0.7':2} #Qualquer outro sai na porta 5
#Lista de Grupos que ja possui o fluxo no Switch
GRUPOS_S1 = []
GRUPOS_S2 = []
GRUPOS_S3 = []
GRUPOS_S4 = []
GRUPOS_S5 = []
#Grafo da Rede
GRAFO = nx.MultiGraph()
GRAFO.add_edge('10.0.0.1','s1',cost=1,index=0)
GRAFO.add_edge('10.0.0.2','s1',cost=1,index=1)
GRAFO.add_edge('10.0.0.3','s1',cost=1,index=2)
GRAFO.add_edge('10.0.0.4','s4',cost=1,index=3)
GRAFO.add_edge('10.0.0.5','s4',cost=1,index=4)
GRAFO.add_edge('10.0.0.6','s5',cost=1,index=5)
GRAFO.add_edge('10.0.0.7','s5',cost=1,index=6)
GRAFO.add_edge('10.0.0.8','s3',cost=1,index=7)
GRAFO.add_edge('10.0.0.9','s3',cost=1,index=8)
GRAFO.add_edge('s1','s2',cost=1,index=9)
GRAFO.add_edge('s3','s2',cost=1,index=10)
GRAFO.add_edge('s4','s2',cost=1,index=11)
GRAFO.add_edge('s5','s2',cost=1,index=12)
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
#Lista de Grupos Multicast com participantes
LISTA_PARTICIPANTES_GRUPO_MULTICAST = []
#Fim Variaveis Globais


class trabalho(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    #_CONTEXTS = {'igmplib': igmplib.IgmpLib}
    #OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(trabalho, self).__init__(*args, **kwargs)
        #self._snoop = kwargs['igmplib']
        #self._snoop.set_querier_mode(
            #dpid=str_to_dpid('0000000000000001'), server_port=2)

    #This function gets triggered before the topology controller flows are added
    #But late enough to be able to remove flows

    '''
    Instala regras na inicializacao
    '''
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        try:
            '''
            Regra de Packet In para Servico Multicast
            '''
            id_switch = datapath.id
            os.system('ovs-ofctl add-flow s' + str(id_switch) + ' priority=40000,dl_type=0x0800,nw_proto=17,tp_dst='+str(PORTA_OFERTA_SERVICO)+',actions=output:controller') #Envia o servico Multicast
            os.system('ovs-ofctl add-flow s' + str(id_switch) + ' priority=40000,dl_type=0x0800,nw_proto=2,actions=output:controller') #Envia Pacotest IGMP para o controlador
            #os.system('ovs-ofctl add-flow s' + str(id_switch) + ' priority=40000,dl_type=0x0800,nw_proto=17,tp_dst='+str(PORTA_MULTICAST)+',actions=output:controller') #Envia o Fluxo Multicast
            '''
            Fim Regra de Packet In para Servico Multicast
            '''
        except Exception as e:
            print(e)
    '''
    Packet IN
    '''
    #Packet In
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    #@set_ev_cls(igmplib.EventPacketIn, MAIN_DISPATCHER)
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
            print('Pacote ARP para: '+pkt_arp.dst_ip)
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
                    global LISTA_PARTICIPANTES_GRUPO_MULTICAST
                    arq = open(path_home+'/SistemasMultimidia/AppRyu/ip_servico_multicast.txt','r')
                    ip_multicast = arq.read()
                    if ip_multicast not in LISTA_GRUPO_MULTICAST:
                        print("Grupos Multicast existentes!!")
                        LISTA_GRUPO_MULTICAST.append(ip_multicast)
                        LISTA_PARTICIPANTES_GRUPO_MULTICAST.append([ip_multicast,str(pkt_ipv4.src)]) #Guarda uma lista de participantes do Grupo Multicast // 1Elem:IP_MULTICAST, 2Elem:IP_SERVIDOR
                        print(LISTA_GRUPO_MULTICAST)
                        print(LISTA_PARTICIPANTES_GRUPO_MULTICAST)
                        #Regra para dropar os pacotes no Swtich ate que tenha clientes
                        switch_onde_esta_ip = self.retornaSwitchIP(str(pkt_ipv4.src))
                        #Pega a ultima parte do ip para montar o MAC Destination
                        #vet = ip_multicast.split('.')
                        #mac_dest = '01:00:5e:00:00:0'+vet[len(vet)-1]
                        #os.system('ovs-ofctl add-flow ' + switch_onde_esta_ip + ' priority=65000,dl_type=0x0800,nw_proto=17,dl_src='+pkt_ethernet.src+',dl_dst='+mac_dest+',nw_src='+str(pkt_ipv4.src)+',nw_dst='+ip_multicast+',tp_dst='+str(PORTA_MULTICAST)+',actions=drop')
                        os.system('ovs-ofctl add-flow ' + switch_onde_esta_ip + ' priority=40000,dl_type=0x0800,nw_proto=17,nw_src='+str(pkt_ipv4.src)+',nw_dst='+ip_multicast+',tp_dst='+str(PORTA_MULTICAST)+',actions=drop')
                        print("Regra de DROP APLICADA!!!")
                        #Grava que o Swtich ja possui o fluxo
                        self.gravaFluxoGrupoSwitch(ip_multicast,switch_onde_esta_ip)

        if pkt_igmp:
            #print('Pacote IGMP!!')
            for i in pkt_igmp.records:
                #print(i.address)
                #print('TYPE = '+str(i.type_))
                if i.type_ == 3: #Leave Multicast
                    #Remove o IP do grupo Multicast
                    if self.removeIPGrupoMulticast(str(i.address),str(pkt_ipv4.src)):
                        print('Leave: '+str(pkt_ipv4.src)+' Group: '+str(i.address))
                        print(LISTA_PARTICIPANTES_GRUPO_MULTICAST)
                        #Remove o Fluxo do Participante
                        #path_server_client = nx.dijkstra_path(GRAFO,ip_server,ip_client,weight='cost')

                elif i.type_ == 4 : #Join Multicast
                    #Adiciona o IP ao grupo Multicast
                    if self.adicionaIPGrupoMulticast(str(i.address),str(pkt_ipv4.src)):
                        print('Join: '+str(pkt_ipv4.src)+' Group: '+str(i.address))
                        print(LISTA_PARTICIPANTES_GRUPO_MULTICAST)
                        #Adiciona o Fluxo ao Participante
                        ip_server = self.buscaIPRealServidorMulticast(str(i.address))
                        ip_client = str(pkt_ipv4.src)
                        ip_grupo = str(i.address)
                        self.addRegraFluxoServerClient(ip_server,ip_client,ip_grupo)
                else:
                    print('Nao Sei!!')
    '''
    FIM Packet IN
    '''

    '''
    Adiciona Regra de fluxo entre servidor e o cliente
    '''
    def addRegraFluxoServerClient(self,ip_server,ip_client,ip_grupo):
        path_server_client = nx.dijkstra_path(GRAFO,ip_server,ip_client,weight='cost') #Grafo do caminho
        print("Caminho entre cliente e servidor!!")
        print(path_server_client)
        switch_caminho = []
        for j in range(1,len(path_server_client)-1):
                switch_caminho.append(path_server_client[j]) # Guarda os Switches ate o cliente
        #Para cada switch verifico se ja possui o fluxo
        if len(switch_caminho) == 1: # Host Cliente esta no mesmo switch do Servidor
            print("Parei Aqui!!")
            #os.system('ovs-ofctl add-flow ' + switch_caminho[0] + ' priority=40000,dl_type=0x0800,nw_proto=17,nw_src='+str(pkt_ipv4.src)+',nw_dst='+ip_multicast+',tp_dst='+str(PORTA_MULTICAST)+',actions=drop')
        else: #Host Cliente esta em outro Switch
            for j in switch_caminho:
                if self.switchPossuiFluxoMulticast(ip_grupo,j):
                    print('Swithc: '+ j +' ja possui o Fluxo')
                else:
                    print('Swithc: '+ j +' nao possui o Fluxo')
    '''
    FIM Adiciona Regra de fluxo entre servidor e o cliente
    '''

    '''
    Verifica se um determinado Switch ja possui o fluxo do grupo
    '''
    def switchPossuiFluxoMulticast(self,ip_grupo_multicast,switch):
        retorno = False
        if switch == 's1':
            if ip_grupo_multicast in GRUPOS_S1:
                retorno = True
        elif switch == 's2':
            if ip_grupo_multicast in GRUPOS_S2:
                retorno = True
        elif switch == 's3':
            if ip_grupo_multicast in GRUPOS_S3:
                retorno = True
        elif switch == 's4':
            if ip_grupo_multicast in GRUPOS_S4:
                retorno = True
        elif switch == 's5':
            if ip_grupo_multicast in GRUPOS_S5:
                retorno = True
        return retorno

    '''
    FIM Verifica se um determinado Switch ja possui o fluxo do grupo
    '''

    '''
    Grava que o Swtich ja possui o trafego de um determinado Grupo
    '''
    def gravaFluxoGrupoSwitch(self,ip_grupo_multicast,switch):
        if switch == 's1':
            global GRUPOS_S1
            GRUPOS_S1.append(ip_grupo_multicast)
        elif switch == 's2':
            global GRUPOS_S2
            GRUPOS_S2.append(ip_grupo_multicast)
        elif switch == 's3':
            global GRUPOS_S3
            GRUPOS_S3.append(ip_grupo_multicast)
        elif switch == 's4':
            global GRUPOS_S4
            GRUPOS_S4.append(ip_grupo_multicast)
        elif switch == 's5':
            global GRUPOS_S5
            GRUPOS_S5.append(ip_grupo_multicast)
    '''
    FIM Grava que o Swtich ja possui o trafego de um determinado Grupo
    '''

    '''
    Busca IP Real do Servidor Multicast
    '''
    def buscaIPRealServidorMulticast(self,ip_grupo_multicast):
        ip_real_servidor = ''
        for i in LISTA_PARTICIPANTES_GRUPO_MULTICAST:
            if i[0] == ip_grupo_multicast:
                ip_real_servidor = i[1]
        return ip_real_servidor

    '''
    FIM Busca IP Real do Servidor Multicast
    '''

    '''
    Adiciona IP ao grupo Multicast
    '''
    def adicionaIPGrupoMulticast(self,ip_grupo,ip_cliente):
        retorno = False
        global LISTA_GRUPO_MULTICAST
        global LISTA_PARTICIPANTES_GRUPO_MULTICAST
        if ip_grupo in LISTA_GRUPO_MULTICAST:
            #IP de servico esta ativo
            for i in LISTA_PARTICIPANTES_GRUPO_MULTICAST:
                if i[0] == ip_grupo:
                    lista = i #Recebe uma lista do Grupo Multicast em questao
                    if ip_cliente not in lista:
                        #Adiciona o ip ao grupo
                        lista.append(ip_cliente)
                        #print(LISTA_PARTICIPANTES_GRUPO_MULTICAST)
                        retorno = True
                    else:
                        retorno = False

        else:
            retorno = False
        return retorno

    '''
    FIM Adiciona IP ao grupo Multicast
    '''

    '''
    Remove IP do grupo Multicast
    '''
    def removeIPGrupoMulticast(self,ip_grupo,ip_cliente):
        retorno = False
        global LISTA_GRUPO_MULTICAST
        global LISTA_PARTICIPANTES_GRUPO_MULTICAST
        if ip_grupo in LISTA_GRUPO_MULTICAST:
            #IP de servico esta ativo
            for i in LISTA_PARTICIPANTES_GRUPO_MULTICAST:
                if i[0] == ip_grupo:
                    lista = i #Recebe uma lista do Grupo Multicast em questao
                    if ip_cliente in lista:
                        #Remove ip do grupo
                        lista.remove(ip_cliente)
                        #print(LISTA_PARTICIPANTES_GRUPO_MULTICAST)
                        retorno = True
                    else:
                        retorno = False

        else:
            retorno = False
        return retorno

    '''
    FIM Remove IP do grupo Multicast
    '''


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
#app_manager.require_app('ryu.app.simple_switch_TrabalhoMultimidia')
app_manager.require_app('ryu.app.simple_switch_13_modTrabalhoMultimidia')
#app_manager.require_app('ryu.app.simple_switch_igmp_13')
#app_manager.require_app('ryu.app.rest_conf_switch')
#app_manager.require_app('ryu.app.rest_topology')
#app_manager.require_app('ryu.app.rest_qos_mod')
