from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import time
from mininet.node import Controller, RemoteController, OVSBridge

class ProgettoTopo(Topo):
    def build(self):
        
        # creo gli host
        eng_svr = self.addHost('eng_srv', ip='10.0.0.1/24')
        mgr_svr = self.addHost('mgr_svr', ip='192.168.1.1/24')

        # host dipartimento architetture
        sens1_arch = self.addHost('s1_arch', ip='11.0.0.1/24')
        sens2_arch = self.addHost('s2_arch', ip='11.0.0.2/24')

        # host dipartimento ingegneria
        sens1_eng = self.addHost('s1_eng', ip='12.0.0.1/24')
        sens2_eng = self.addHost('s2_eng', ip='12.0.0.2/24')

        # host dipartimento lettere
        sens1_lit = self.addHost('s1_lit', ip='10.8.1.1/24')
        sens2_lit = self.addHost('s2_lit', ip='10.8.1.2/24')
        
        # creo gli switch
        R1 = self.addSwitch('R1', dpid='0000000000000001')
        R2 = self.addSwitch('R2', dpid='0000000000000002')
        R3 = self.addSwitch('R3', dpid='0000000000000003')
        R4 = self.addSwitch('R4', dpid='0000000000000004')
        R5 = self.addSwitch('R5', dpid='0000000000000005')


        # switch dipartimento architetture
        sw_arch = self.addSwitch('sw_arch', cls=OVSBridge, dpid='0000000000000006')

        #switch dipartimento ingegneria
        sw_eng = self.addSwitch('sw_eng', cls=OVSBridge, dpid='0000000000000007')

        # switch dipartimento lettere
        sw_lit = self.addSwitch('sw_lit', cls=OVSBridge, dpid='0000000000000008')

        # creo i link
        self.addLink(eng_svr, R1, bw=100, delay='5ms')
        self.addLink(R3, mgr_svr, bw=100, delay='5ms')
        self.addLink(R1, R2, bw=20, delay='2ms')
        self.addLink(R2, R5, bw=20, delay='2ms')
        self.addLink(R1, R3, bw=20, delay='2ms')
        self.addLink(R3, R4, bw=20, delay='2ms')

        # link dipartimento archietture
        self.addLink(sens1_arch, sw_arch, bw=1, delay='10ms')
        self.addLink(sens2_arch, sw_arch, bw=1, delay='10ms')
        self.addLink(sw_arch, R2, bw=1, delay='10ms')

        # link dipartimento ingegneria
        self.addLink(sens1_eng, sw_eng, bw=1, delay='10ms')
        self.addLink(sens2_eng, sw_eng, bw=1, delay='10ms')
        self.addLink(sw_eng, R5, bw=1, delay='10ms')

        # link dipartimento lettere
        self.addLink(sens1_lit, sw_lit, bw=100, delay='6ms')
        self.addLink(sens2_lit, sw_lit, bw=100, delay='6ms')
        self.addLink(sw_lit, R4, bw=100, delay='6ms')

if __name__ == '__main__':
    setLogLevel('info')
    topo = ProgettoTopo()
    net = Mininet(topo=topo, link=TCLink, build=False, controller=None)
    net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    net.build()
    net.start()

    # eng server
    net.get('eng_srv').cmd('ip route add default via 10.0.0.254')

    # dipartimento architettura
    net.get('s1_arch').cmd('ip route add default via 11.0.0.254')
    net.get('s2_arch').cmd('ip route add default via 11.0.0.254')

    # dipartimento ingegneria
    net.get('s1_eng').cmd('ip route add default via 12.0.0.254')
    net.get('s2_eng').cmd('ip route add default via 12.0.0.254')

    # dipartimento lettere
    net.get('s1_lit').cmd('ip route add default via 10.8.1.254')
    net.get('s2_lit').cmd('ip route add default via 10.8.1.254')

    # manager server
    net.get('mgr_svr').cmd('ip route add default via 192.168.1.254')

    time.sleep(3) # timeout di 3 secondi per Ryu

    # R1 gateway per Eng server
    net.get('c0').cmd('curl -X POST -d \'{"address": "10.0.0.254/24"}\' http://localhost:8080/router/0000000000000001')

    # R2 gateway per dipartimento architettura
    net.get('c0').cmd('curl -X POST -d \'{"address": "11.0.0.254/24"}\' http://localhost:8080/router/0000000000000002')

    # R3 gateway per manager server
    net.get('c0').cmd('curl -X POST -d \'{"address": "192.168.1.254/24"}\' http://localhost:8080/router/0000000000000003')

    # R4 gateway per dipartimento lettere
    net.get('c0').cmd('curl -X POST -d \'{"address": "10.8.1.254/24"}\' http://localhost:8080/router/0000000000000004')
    
    # R5 gateway per dipartimento ingegneria
    net.get('c0').cmd('curl -X POST -d \'{"address": "12.0.0.254/24"}\' http://localhost:8080/router/0000000000000005')

    # RETI DI TRANSITO TRA I ROUTER

    # R1 - R2 (Subnet: 180.0.0.0/30 -> IP validi: .1, .2)
    net.get('c0').cmd('curl -X POST -d \'{"address": "180.0.0.1/30"}\' http://localhost:8080/router/0000000000000001')
    net.get('c0').cmd('curl -X POST -d \'{"address": "180.0.0.2/30"}\' http://localhost:8080/router/0000000000000002')

    # R1 - R3 (Subnet: 200.0.0.0/30 -> IP validi: .1, .2)
    net.get('c0').cmd('curl -X POST -d \'{"address": "200.0.0.1/30"}\' http://localhost:8080/router/0000000000000001')
    net.get('c0').cmd('curl -X POST -d \'{"address": "200.0.0.2/30"}\' http://localhost:8080/router/0000000000000003')

    # R2 - R5 (Subnet shiftata a 180.0.0.4/30 per evitare conflitti su R2 -> IP validi: .5, .6)
    net.get('c0').cmd('curl -X POST -d \'{"address": "180.0.0.5/30"}\' http://localhost:8080/router/0000000000000002')
    net.get('c0').cmd('curl -X POST -d \'{"address": "180.0.0.6/30"}\' http://localhost:8080/router/0000000000000005')

    # R3 - R4 (Corretta da /32 a /30 -> IP validi: .1, .2)
    net.get('c0').cmd('curl -X POST -d \'{"address": "170.0.0.1/30"}\' http://localhost:8080/router/0000000000000003')
    net.get('c0').cmd('curl -X POST -d \'{"address": "170.0.0.2/30"}\' http://localhost:8080/router/0000000000000004')

    # --- TABELLE DI ROUTING STATICO ---

    # R1 deve sapere che per arrivare ad architettura e ingegneria deve passare per R2 (.2)
    net.get('c0').cmd('curl -X POST -d \'{"destination": "11.0.0.0/24", "gateway": "180.0.0.2"}\' http://localhost:8080/router/0000000000000001') 
    net.get('c0').cmd('curl -X POST -d \'{"destination": "12.0.0.0/24", "gateway": "180.0.0.2"}\' http://localhost:8080/router/0000000000000001') 

    # R1 deve sapere che per arrivare al manager server e a lettere deve passare per R3 (.2)
    net.get('c0').cmd('curl -X POST -d \'{"destination": "192.168.1.0/24", "gateway": "200.0.0.2"}\' http://localhost:8080/router/0000000000000001') 
    net.get('c0').cmd('curl -X POST -d \'{"destination": "10.8.1.0/24", "gateway": "200.0.0.2"}\' http://localhost:8080/router/0000000000000001') 

    # R4 e R5 mandano pacchetti a un indirizzo di default: se non sai a chi spedire, spedisci a R3/R2
    net.get('c0').cmd('curl -X POST -d \'{"destination": "0.0.0.0/0", "gateway": "170.0.0.1"}\' http://localhost:8080/router/0000000000000004') # Spedisce a R3 (.1)
    net.get('c0').cmd('curl -X POST -d \'{"destination": "0.0.0.0/0", "gateway": "180.0.0.5"}\' http://localhost:8080/router/0000000000000005') # Spedisce a R2 (.5)

    # R2 manda a ingegneria passando per R5 (.6)
    net.get('c0').cmd('curl -X POST -d \'{"destination": "12.0.0.0/24", "gateway": "180.0.0.6"}\' http://localhost:8080/router/0000000000000002')

    # R2 manda a R1 (.1) cio' che non conosce
    net.get('c0').cmd('curl -X POST -d \'{"destination": "0.0.0.0/0", "gateway": "180.0.0.1"}\' http://localhost:8080/router/0000000000000002')

    # analogo per R3
    net.get('c0').cmd('curl -X POST -d \'{"destination": "10.8.1.0/24", "gateway": "170.0.0.2"}\' http://localhost:8080/router/0000000000000003') # Spedisce a R4 (.2)
    net.get('c0').cmd('curl -X POST -d \'{"destination": "0.0.0.0/0", "gateway": "200.0.0.1"}\' http://localhost:8080/router/0000000000000003') # Spedisce a R1 (.1)

    # Consentire il traffico di Eng_server esclusivamente verso il dipartimento di ingegneria
    net.get('eng_srv').cmd('iptables -A OUTPUT -d 12.0.0.0/24 -j ACCEPT')
    
    # Negare il traffico da Eng_server verso gli altri dipartimenti
    net.get('eng_srv').cmd('iptables -A OUTPUT -d 11.0.0.0/24 -j DROP') # Architettura
    net.get('eng_srv').cmd('iptables -A OUTPUT -d 10.8.1.0/24 -j DROP') # Lettere

    # Avvio di Flask
    net.get('mgr_svr').cmd('python3 manager_server.py &')

    # sensori demoni 
    net.get('s1_arch').cmd('python3 sensor_daemon.py Arch_sens1 &')
    net.get('s2_arch').cmd('python3 sensor_daemon.py Arch_sens2 &')
    net.get('s1_eng').cmd('python3 sensor_daemon.py Eng_sens1 &')
    net.get('s2_eng').cmd('python3 sensor_daemon.py Eng_sens2 &')
    net.get('s1_lit').cmd('python3 sensor_daemon.py Lit_sens1 &')
    net.get('s2_lit').cmd('python3 sensor_daemon.py Lit_sens2 &')

    CLI(net)
    net.stop()