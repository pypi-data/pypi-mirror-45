## Test Steps:
    #Step 1: Create a session and connect to two back to back stc ports
    #Step 2: Configue 2 isisv4 devices on each port
    #Step 3: Configure 2 isisv4 routes one each isis device
    #Step 4: Configure traffic group between two isis devices
    #Step 5: Save the configuration as an XML file
    #Step 6: Start the isis devices
    #Step 7: Start the traffic
    #Step 8: Validate the isis stats
    #Step 7: Validate the traffic stats
    #Step 8: Delete session and release resources

from openhltspirent import Openhltest
import time
import sys

#Commandline arguments
serverip=sys.argv[1]
chassisip=sys.argv[2]
sessionname=sys.argv[3]
portnumber=sys.argv[4]

print("ohtweb server ip", serverip)
print("chassis ip", chassisip)
print("session name", sessionname)
print("port number",portnumber)

# connect openhltest server
opt = Openhltest(serverip,portnumber)

try:
    session = opt.sessions(sessionname)
    session.delete()
    print("######## Deleted existing session with name %s  ######### \n" % sessionname)
except:
    print("######## There is no session exist with name %s ######## \n" % sessionname)

# create session : "ISISV4 Demo"
session = opt.create_sessions(sessionname)

#  step 1. create and connect two ports
print('\n  step 1. create and connect two ports\n')
config = session.config()

port1 = config.create_ports('Ethernet1')
port1.location = chassisip + r'/1/1'
port1.update()

port2 = config.create_ports('Ethernet2')
port2.location = chassisip + r'/1/2'
port2.update()

port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'CONNECT'
config.port_control(port_control_input)

#  step 2. create two devices under the port1, protocol stack: eth/vlan/vlan/ipv4/isisv4. 
print('\n  step 2. create two devices under the port1, protocol stack: eth/vlan/vlan/ipv4/isisv4.\n')
# create device groups: 'EastSideDevicegroup1' under the port 'Ethernet1'
device_group_east = config.create_device_groups('EastSideDevicegroup1')
device_group_east.ports = ['Ethernet1']
device_group_east.update()

# create devices: 'Devices 1' under the device_group_east
devices_1 = device_group_east.create_devices('Device1')

# set device count
devices_1.device_count_per_port = 1
devices_1.update()


# create protocols ethernet
protocol_eth_1 = devices_1.create_protocols('Ethernet1')
protocol_eth_1.protocol_type = 'ETHERNET'
protocol_eth_1.update()

# create protocols vlan outer
protocol_vlan_1 = devices_1.create_protocols('Vlan1')
protocol_vlan_1.protocol_type = 'VLAN'
protocol_vlan_1.parent_link = 'Ethernet1'
protocol_vlan_1.update()

# create protocols vlan inner
protocol_vlan_2 = devices_1.create_protocols('Vlan2')
protocol_vlan_2.protocol_type = 'VLAN'
protocol_vlan_2.parent_link = 'Vlan1'
protocol_vlan_2.update()

# create protocols IPv4
protocol_ipv4_1 = devices_1.create_protocols('IPV41')
protocol_ipv4_1.protocol_type = 'IPV4'
protocol_ipv4_1.parent_link = 'Vlan2'
protocol_ipv4_1.update()

# config mac addr
eth_1 = protocol_eth_1.ethernet()
eth_1.update()

eth_1_mac = eth_1.mac()
eth_1_mac.pattern_type = 'INCREMENT'
eth_1_mac.update()

eth_1_mac_incr = eth_1_mac.increment()
eth_1_mac_incr.start = '00:10:94:00:00:01'
eth_1_mac_incr.step = '00:00:00:00:00:01'
eth_1_mac_incr.update()

# config ipv4 address
ipv4_1 = protocol_ipv4_1.ipv4()
ipv4_1.update()

#ipv4_1.source_address = '192.85.1.3'
ipv4_1_src_addr = ipv4_1.source_address()
ipv4_1_src_addr.pattern_type = 'SINGLE'
ipv4_1_src_addr.single = '192.85.1.3'
ipv4_1_src_addr.update()

ipv4_1_gw_addr = ipv4_1.gateway_address()
ipv4_1_gw_addr.pattern_type = 'SINGLE'
ipv4_1_gw_addr.single = '192.85.1.13'
ipv4_1_gw_addr.update()

#create and config ISISv4 protocol
protocol_isisv4_1 = devices_1.create_protocols('ISISV41')
protocol_isisv4_1.protocol_type = 'ISIS'
protocol_isisv4_1.parent_link = 'IPV41'
protocol_isisv4_1.update()

isisv4 = protocol_isisv4_1.isis()
isisv4.update()

system_id = isisv4.system_id()
system_id.single = '00:10:94:00:00:01'
system_id.update()

router_priority = isisv4.router_priority()
router_priority.single = '1'
router_priority.update()

network_type = isisv4.network_type()
network_type.single = 'BROADCAST'
network_type.update()

hello_interval = isisv4.hello_interval()
hello_interval.single = '10'
hello_interval.update()

level = isisv4.level()
level.single = 'L2'
level.update()

#ISISv4 route creation on ISISv4 device
simulated_networks_1 = device_group_east.create_simulated_networks('SimulatedNetworks1')
simulated_networks_1.device_count_per_port = 1
simulated_networks_1.parent_link = 'Device1'
simulated_networks_1.update()

# create 'ISISV4 Route Range' under the simulated_networks_1
networks_1 = simulated_networks_1.create_networks('ISISV4Networks1')
networks_1.flow_link = 'ISISV41'
networks_1.network_type = 'ISIS_ROUTE_RANGE'
networks_1.update()

#config the isisv4_route_range_1
isisv4_route_range_1 = networks_1.isis_route_range()    
isisv4_route_range_1.update()

system_id_route = isisv4_route_range_1.system_id()
system_id_route.single = '00:10:94:00:10:01'
system_id_route.update()

isisv4_routes1 = isisv4_route_range_1.create_ipv4_routes('isisv4route1')
isisv4_routes1.update()

address = isisv4_routes1.address()
address.pattern_type = 'SINGLE'
address.single = '192.0.1.0'
address.update()

# ISISV4 Device configuration on port2
device_group_west = config.create_device_groups('WestSideDevicegroup1')
device_group_west.ports = ['Ethernet2']
device_group_west.update()

# create devices: 'Devices 2' under the device_group_west
devices_2 = device_group_west.create_devices('Device2')

# set device count
devices_2.device_count_per_port = 1
devices_2.update()

# create protocols ethernet
protocol_eth_2 = devices_2.create_protocols('WestEthernet2')
protocol_eth_2.protocol_type = 'ETHERNET'
protocol_eth_2.update()

# create protocols vlan outer
protocol_vlan_3 = devices_2.create_protocols('WestVlan1')
protocol_vlan_3.protocol_type = 'VLAN'
protocol_vlan_3.parent_link = 'WestEthernet2'
protocol_vlan_3.update()

# create protocols vlan inner
protocol_vlan_4 = devices_2.create_protocols('WestVlan2')
protocol_vlan_4.protocol_type = 'VLAN'
protocol_vlan_4.parent_link = 'WestVlan1'
protocol_vlan_4.update()

# create protocols IPv4
protocol_ipv4_2 = devices_2.create_protocols('IPV42')
protocol_ipv4_2.protocol_type = 'IPV4'
protocol_ipv4_2.parent_link = 'WestVlan2'
protocol_ipv4_2.update()

# config mac addr
eth_2 = protocol_eth_2.ethernet()
eth_2.update()

eth_2_mac = eth_1.mac()
eth_2_mac.pattern_type = 'INCREMENT'
eth_2_mac.update()

eth_2_mac_incr = eth_2_mac.increment()
eth_2_mac_incr.start = '00:10:94:00:10:01'
eth_2_mac_incr.step = '00:00:00:00:00:01'
eth_2_mac_incr.update()

# config ipv4 address
ipv4_2 = protocol_ipv4_2.ipv4()
ipv4_2.update()

#ipv4_1.source_address = '192.85.1.3'
ipv4_2_src_addr = ipv4_2.source_address()
ipv4_2_src_addr.pattern_type = 'SINGLE'
ipv4_2_src_addr.single = '192.85.1.13'
ipv4_2_src_addr.update()

ipv4_2_gw_addr = ipv4_2.gateway_address()
ipv4_2_gw_addr.pattern_type = 'SINGLE'
ipv4_2_gw_addr.single = '192.85.1.3'
ipv4_2_gw_addr.update()

#create and config ISISv4 protocol
protocol_isisv4_2 = devices_2.create_protocols('ISISV42')
protocol_isisv4_2.protocol_type = 'ISIS'
protocol_isisv4_2.parent_link = 'IPV42'
protocol_isisv4_2.update()

isisv4 = protocol_isisv4_2.isis()
isisv4.update()

system_id = isisv4.system_id()
system_id.single = '00:20:94:00:00:01'
system_id.update()

router_priority = isisv4.router_priority()
router_priority.single = '1'
router_priority.update()

network_type = isisv4.network_type()
network_type.single = 'BROADCAST'
network_type.update()

hello_interval = isisv4.hello_interval()
hello_interval.single = '10'
hello_interval.update()

level = isisv4.level()
level.single = 'L2'
level.update()

#ISISv4 route creation on ISISv4 device
simulated_networks_2 = device_group_west.create_simulated_networks('SimulatedNetworks2')
simulated_networks_2.device_count_per_port = 1
simulated_networks_2.parent_link = 'Device2'
simulated_networks_2.update()

# create 'ISISV4 Route Range' under the simulated_networks_2
networks_2 = simulated_networks_2.create_networks('ISISV4Networks2')
networks_2.flow_link = 'ISISV42'
networks_2.network_type = 'ISIS_ROUTE_RANGE'
networks_2.update()

#config the isisv4_route_range_2
isisv4_route_range_2 = networks_2.isis_route_range()
isisv4_route_range_2.update()

system_id_route = isisv4_route_range_2.system_id()
system_id_route.single = '00:10:94:00:20:01'
system_id_route.update()

isisv4_routes2 = isisv4_route_range_2.create_ipv4_routes('isisv4route2')
isisv4_routes2.update()

address = isisv4_routes2.address()
address.pattern_type = 'SINGLE'
address.single = '192.0.1.0'
address.update()

#  start ISISv4 protocol
print('\n  start ISISV4 protocol\n')
isisv4_control_input1 = config.IsisControlInput()
isisv4_control_input1.mode = 'START'
config.isis_control(isisv4_control_input1)

print('\n  Waiting for 60 secs to establish desired state\n')
time.sleep(60)

#   Get the ISISv4 statistics
print('\n  Get the ISISv4 statistics\n')
statistics = session.statistics()

isisv4_statistics_1 = statistics.isis_statistics('Device1')
isisv4_statistics_2 = statistics.isis_statistics('Device2')
print(isisv4_statistics_1._values)
print(isisv4_statistics_2._values)

isis1_state = isisv4_statistics_1._values['router-state']
isis2_state = isisv4_statistics_2._values['router-state']

if (isis1_state == 'UP'and isis2_state == 'UP') :
    print('*' * 40)
    print ("\n Info :ISIS session established successful \n")
    print('*' * 40)
else :
    print ("\n <error> Failed to establish isis sessions")
    sys.exit();

# create BOUND streamblock - IPv4 endpoints
device_traffic = config.create_device_traffic('IPV4Stream1')

# ENPOINTS: Devices
device_traffic.encapsulation = "IPV4"
device_traffic.sources = ['SimulatedNetworks1']
device_traffic.destinations = ['SimulatedNetworks2']
device_traffic.bidirectional='true'
device_traffic.update()

#Config Frame Size
frame_length_1 = device_traffic.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '512'
frame_length_1.update()

#  start traffic
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('IPV4Stream1')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

time.sleep(5)

traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('IPV4Stream1')
traffic_control_input1.mode = 'STOP'
config.traffic_control(traffic_control_input1)

#  Get the traffic statistics
print('\n  Get traffic statistics\n')
statistics = session.statistics()
traffic_statistics_1 = statistics.device_traffic('IPV4Stream1')
print(traffic_statistics_1._values)

tx_frames = traffic_statistics_1._values['tx-frames']
rx_frames = traffic_statistics_1._values['rx-frames']

if (tx_frames == rx_frames):
    print('*' * 40)
    print ("\n Info: Traffic is transmitted successfully \n")
    print('*' * 40)
else :
    print ("\n <error> Traffic is not transmitted successfully")
    sys.exit();

# stop the ISISv4 protocol
print('\n  stop ISISv4 protocol\n')
isisv4_control_input2 = config.IsisControlInput()
isisv4_control_input2.targets.append('ISISV41')
isisv4_control_input2.targets.append('ISISV42')
isisv4_control_input2.mode = 'STOP'
config.isis_control(isisv4_control_input2) 


port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)
session.delete()

print ("COMPLETED................")
