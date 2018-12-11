#!/usr/bin/python
import os
IP_CONTROLADOR = '10.0.0.99' #Ip do controlador

'''
Regras de Links Principal
'''
#s1
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:01,actions=output:1')
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:02,actions=output:2')
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:03,actions=output:3')
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:04,actions=output:7')
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:05,actions=output:7')
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:06,actions=output:7')
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:07,actions=output:7')
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:08,actions=output:7')
os.system('ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:09,actions=output:7')

#s3
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:08,actions=output:1')
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:09,actions=output:2')
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:01,actions=output:7')
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:02,actions=output:7')
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:03,actions=output:7')
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:04,actions=output:7')
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:05,actions=output:7')
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:06,actions=output:7')
os.system('ovs-ofctl add-flow s3 dl_dst=00:00:00:00:00:07,actions=output:7')

#s4
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:04,actions=output:1')
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:05,actions=output:2')
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:01,actions=output:6')
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:02,actions=output:6')
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:03,actions=output:6')
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:06,actions=output:7')
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:07,actions=output:7')
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:08,actions=output:7')
os.system('ovs-ofctl add-flow s4 dl_dst=00:00:00:00:00:09,actions=output:7')

#s5
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:06,actions=output:1')
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:07,actions=output:2')
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:01,actions=output:6')
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:02,actions=output:6')
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:03,actions=output:6')
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:04,actions=output:6')
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:05,actions=output:6')
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:08,actions=output:7')
os.system('ovs-ofctl add-flow s5 dl_dst=00:00:00:00:00:09,actions=output:7')

'''
Sem essas regras, a rede eh inundada com pacotes UDP de fornecimento de servico
'''

#Direcionar todo pacote UDP para nao atrapalhar o Multicast S1
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.1,nw_dst='+IP_CONTROLADOR+',actions=output:controller')
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.2,nw_dst='+IP_CONTROLADOR+',actions=output:controller')
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.3,nw_dst='+IP_CONTROLADOR+',actions=output:controller')
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.4,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.5,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.6,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.7,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.8,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s1 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.9,nw_dst='+IP_CONTROLADOR+',actions=drop')


#Direcionar todo pacote UDP para nao atrapalhar o Multicast S3
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.1,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.2,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.3,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.4,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.5,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.6,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.7,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.8,nw_dst='+IP_CONTROLADOR+',actions=output:controller')
os.system('ovs-ofctl add-flow s3 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.9,nw_dst='+IP_CONTROLADOR+',actions=output:controller')

#Direcionar todo pacote UDP para nao atrapalhar o Multicast S4
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.1,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.2,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.3,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.4,nw_dst='+IP_CONTROLADOR+',actions=output:controller')
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.5,nw_dst='+IP_CONTROLADOR+',actions=output:controller')
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.6,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.7,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.8,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s4 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.9,nw_dst='+IP_CONTROLADOR+',actions=drop')

#Direcionar todo pacote UDP para nao atrapalhar o Multicast S5
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.1,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.2,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.3,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.4,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.5,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.6,nw_dst='+IP_CONTROLADOR+',actions=output:controller')
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.7,nw_dst='+IP_CONTROLADOR+',actions=output:controller')
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.8,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s5 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.9,nw_dst='+IP_CONTROLADOR+',actions=drop')

#Direcionar todo pacote UDP para nao atrapalhar o Multicast S2
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.1,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.2,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.3,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.4,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.5,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.6,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.7,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.8,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src='+IP_CONTROLADOR+',nw_dst=10.0.0.9,actions=drop')

#Direcionar todo pacote UDP para nao atrapalhar o Multicast S2
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.1,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.2,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.3,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.4,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.5,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.6,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.7,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.8,nw_dst='+IP_CONTROLADOR+',actions=drop')
os.system('ovs-ofctl add-flow s2 priority=60000,dl_type=0x0800,nw_proto=17,nw_src=10.0.0.9,nw_dst='+IP_CONTROLADOR+',actions=drop')

'''
Sem essas regras, a rede eh inundada com pacotes IGMP
'''
#Drop IGMP sem necessidade s1
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.1,nw_dst=224.0.0.0/24,actions=output:controller')
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.2,nw_dst=224.0.0.0/24,actions=output:controller')
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.3,nw_dst=224.0.0.0/24,actions=output:controller')
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.4,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.5,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.6,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.7,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.8,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s1 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.9,nw_dst=224.0.0.0/24,actions=drop')


#Drop IGMP sem necessidade s2
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.1,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.2,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.3,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.4,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.5,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.6,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.7,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.8,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s2 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.9,nw_dst=224.0.0.0/24,actions=drop')

#Drop IGMP sem necessidade s3
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.1,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.2,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.3,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.4,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.5,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.6,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.7,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.8,nw_dst=224.0.0.0/24,actions=output:controller')
os.system('ovs-ofctl add-flow s3 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.9,nw_dst=224.0.0.0/24,actions=output:controller')

#Drop IGMP sem necessidade s4
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.1,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.2,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.3,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.4,nw_dst=224.0.0.0/24,actions=output:controller')
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.5,nw_dst=224.0.0.0/24,actions=output:controller')
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.6,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.7,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.8,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s4 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.9,nw_dst=224.0.0.0/24,actions=drop')

#Drop IGMP sem necessidade s5
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.1,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.2,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.3,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.4,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.5,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.6,nw_dst=224.0.0.0/24,actions=output:controller')
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.7,nw_dst=224.0.0.0/24,actions=output:controller')
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.8,nw_dst=224.0.0.0/24,actions=drop')
os.system('ovs-ofctl add-flow s5 priority=50000,dl_type=0x0800,nw_proto=2,nw_src=10.0.0.9,nw_dst=224.0.0.0/24,actions=drop')
