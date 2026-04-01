from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Controller, RemoteController
from mininet.cli import CLI

class ProgettoTopo(Topo):
    def build(self):
        
        # creo gli host
        eng_server = self.addHost('eng_server', ip='10.0.0.1/24')

        # host dipartimento architetture
        sens1_arch = self.addHost('sens1_arch', ip='11.0.0.1/24')
        sens2_arch = self.addHost('sens2_arch', ip='11.0.0.2/24')
        
        # creo gli switch
        R1 = self.addSwitch('R1')
        R2 = self.addSwitch('R2')

        # switch dipartimento architetture
        sw_arch = self.addSwitch('sw_arch')

        # creo i link
        self.addLink(eng_server, R1, bw=100, delay='5ms')
        self.addLink(R1, R2, bw=20, delay='2ms')

        # link dipartimento archietture
        self.addLink(sens1_arch, sw_arch, bw=1, delay='10ms')
        self.addLink(sens2_arch, sw_arch, bw=1, delay='10ms')
        self.addLink(sw_arch, R2, bw=1, delay='10ms')
