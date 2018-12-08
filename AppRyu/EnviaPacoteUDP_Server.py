#!/usr/bin/python2

from scapy.all import *
import os
path_home = os.getenv("HOME") #Captura o caminho da pasta HOME

print("Digite o IP Multicast que deseja oferta o servico!!!")
ip_multicast_servico = raw_input("Digite o IP_MULTICAST:")
#dest = raw_input("\nDestination: ")
#destport = input("Destination port: ") #Porta de destino

dest = '10.0.0.99'
destport = '23000'
ip = IP(dst=dest)
udp = UDP(dport=int(destport),sport=40000)
pkt = ip/udp
t = sr(pkt)
print(t)

arq = open(path_home+'/SistemasMultimidia/AppRyu/ip_servico_multicast.txt', 'w')
arq.writelines(ip_multicast_servico)
arq.close()
