#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from mininet.util import dumpNodeConnections
from subprocess import call

import os
import time
import subprocess

path_home = os.getenv("HOME") #Captura o caminho da pasta HOME

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   #autoSetMacs=True,
                   host=CPULimitedHost,
                   link=TCLink,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4')
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6')
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7')
    srv1 = net.addHost('srv1', cls=Host, ip='10.0.0.8')
    srv2 = net.addHost('srv2', cls=Host, ip='10.0.0.9')


    info( '*** Add links\n')
    net.addLink(h1, s1, 1, 1)
    net.addLink(h2, s1, 1, 2)
    net.addLink(h3, s1, 1, 3)
    net.addLink(srv1, s3, 1, 1)
    net.addLink(srv2, s3, 1, 2)
    net.addLink(h4, s4, 1, 1)
    net.addLink(h5, s4, 1, 2)
    net.addLink(h6, s5, 1, 1)
    net.addLink(h7, s5, 1, 2)
    net.addLink(s1, s2, 5, 1)
    net.addLink(s3, s2, 5, 2)
    net.addLink(s4, s2, 5, 3)
    net.addLink(s5, s2, 5, 4)



    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])

    info( '*** Setting routes\n')
    h1.cmd('route add default dev h1-eth1')
    h2.cmd('route add default dev h2-eth1')
    h3.cmd('route add default dev h3-eth1')
    h4.cmd('route add default dev h4-eth1')
    h5.cmd('route add default dev h5-eth1')
    h6.cmd('route add default dev h6-eth1')
    h7.cmd('route add default dev h7-eth1')
    srv1.cmd('route add default dev srv1-eth1')
    srv2.cmd('route add default dev srv2-eth1')


    info( '*** Post configure switches and hosts\n')
    dumpNodeConnections(net.hosts)
    #Instala as filas de QoS
    #os.system('python '+path_home+'/ryu/Bruno/admin.py &')
    #time.sleep(4)
    #print("Filas guardadas no Open vSwitch!!! \n")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
