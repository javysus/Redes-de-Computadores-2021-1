from mininet.topo import Topo

class Red1( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        host1 = self.addHost( 'h1', mac = '00:00:00:00:00:01')
        host2 = self.addHost( 'h2', mac = '00:00:00:00:00:02' )
        host3 = self.addHost( 'h3', mac = '00:00:00:00:00:03' )
        host4 = self.addHost( 'h4', mac = '00:00:00:00:00:04' )
        host5= self.addHost( 'h5', mac = '00:00:00:00:00:05' )
        host6 = self.addHost( 'h6', mac = '00:00:00:00:00:06')

        switch1 = self.addSwitch( 's1',dpid="1")
        switch2 = self.addSwitch( 's2', dpid="2")
        switch3 = self.addSwitch( 's3', dpid="3")
        switch4 = self.addSwitch( 's4', dpid="4")

        host7 = self.addHost('h7', mac = '00:00:00:00:00:07')
        host8 = self.addHost('h8', mac = '00:00:00:00:00:08')
        # Add links

        self.addLink(host1,switch1,0,1)
        self.addLink(host2,switch1,0,2)

        self.addLink(host3,switch2,0,3)
        self.addLink(host4,switch2,0,4)

        self.addLink(host5,switch3,0,5)
        self.addLink(host6,switch3,0,6)

        self.addLink(switch1,switch2,7,8)
        self.addLink(switch2,switch3,9,10)

        self.addLink(switch1,switch4,11,12)
        self.addLink(switch3,switch4,13,14)

        self.addLink(switch4,host7,15,0)
        self.addLink(switch4,host8,17,0)

class Red2( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        host1 = self.addHost( 'h1', mac = '00:00:00:00:00:01')
        host2 = self.addHost( 'h2', mac = '00:00:00:00:00:02' )
        host3 = self.addHost( 'h3', mac = '00:00:00:00:00:03' )
        host4 = self.addHost( 'h4', mac = '00:00:00:00:00:04' )
        host5= self.addHost( 'h5', mac = '00:00:00:00:00:05' )
        host6 = self.addHost( 'h6', mac = '00:00:00:00:00:06')

        switch1 = self.addSwitch( 's1',dpid="1")
        switch2 = self.addSwitch( 's2', dpid="2")
        switch3 = self.addSwitch( 's3', dpid="3")
        switch4 = self.addSwitch( 's4', dpid="4")
        switch5 = self.addSwitch( 's5', dpid="5")

        # Add links

        #Host 1 y 2 a Switch 1
        self.addLink(host1,switch1,0,1)
        self.addLink(host2,switch1,0,2)

        #Host 3 y 4 a Switch 2
        self.addLink(host3,switch2,0,3)
        self.addLink(host4,switch2,0,4)

        #Host 5 y 6 a Switch 5
        self.addLink(host5,switch5,0,5)
        self.addLink(host6,switch5,0,6)

        self.addLink(switch2,switch1,7,8)
        self.addLink(switch1,switch5,9,10)
        self.addLink(switch5,switch3,11,12)
        self.addLink(switch3,switch4,13,14)
        self.addLink(switch4,switch2,15,16)
        self.addLink(switch3,switch1,17,18)

topos = { 'Red1': ( lambda: Red1() ), 'Red2': ( lambda: Red2() ) }