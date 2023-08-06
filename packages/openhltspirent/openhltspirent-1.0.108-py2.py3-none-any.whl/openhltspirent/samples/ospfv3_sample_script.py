##Test Steps
    #Step 1:  Create a session and connect to two back to back stc ports
    #Step 2:  Configue ospfv3 devices on each port
    #Step 3:  Configure ospfv3 routes one each ospf device
    #Step 4:  Configure traffic group between two ospf devices
    #Step 5:  Save the configuration as an XML file
    #Step 6:  Start the ospf devices
    #Step 7:  Start the traffic
    #Step 8:  Validate the ospf stats
    #Step 9:  Validate the traffic stats
    #Step 10: Delete session and release resources

from openhltspirent import Openhltest
import time
import sys

QEMU_DBG = False

#Commandline arguments
serverip=sys.argv[1]
chassisip=sys.argv[2]
sessionname=sys.argv[3]
portnumber=sys.argv[4]

if chassisip == '0.0.0.0':
    QEMU_DBG = True

if QEMU_DBG:
    chassisip_1 = '10.61.67.21'
    chassisip_2 = '10.61.67.81'

print("ohtweb server ip", serverip)
if QEMU_DBG:
    print("chassis ip", chassisip_1, chassisip_2)
else:    
    print("chassis ip", chassisip)
print("session name", sessionname)
print("port number", portnumber)

opt = Openhltest(serverip,portnumber)

try:
    session = opt.sessions(sessionname)
    session.delete()
    print("######## Deleted existing session with name %s ######### \n" % sessionname)
except:
    print("######## There is no session exist with name  %s ######### \n" % sessionname)

# create session : 
session = opt.create_sessions(name = sessionname)

#  step 1. create and connect two ports
print('\n  step 1. create and connect two ports\n')
config = session.config()

port1 = config.create_ports('Ethernet1')
if QEMU_DBG:
    port1.location = chassisip_1 + r'/1/1'
else:
    port1.location = chassisip + r'/1/1'
port1.update()

port2 = config.create_ports('Ethernet2')
if QEMU_DBG:
    port2.location = chassisip_2 + r'/1/1'
else:    
    port2.location = chassisip + r'/1/2'
port2.update()

port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'CONNECT'
config.port_control(port_control_input)

#  step 2. create two devices under the port1, protocol stack: eth/vlan/vlan/ipv6/ospfv3. 
print('\n  step 2. create two devices under the port1, protocol stack: eth/vlan/vlan/ipv6/ospfv3.\n')
# create device groups: 'East Side - Device group 1' under the port 'Ethernet - 001'
device_group_east = config.create_device_groups('EastSideDevicegroup1')
device_group_east.ports = ['Ethernet1']
device_group_east.update()

# create devices: 'Devices 1' under the device_group_east
devices_1 = device_group_east.create_devices('Device1')

# create protocols ethernet
protocol_eth_1 = devices_1.create_protocols('ProtocolEthernet1')
protocol_eth_1.protocol_type = 'ETHERNET'
protocol_eth_1.update()

# create protocols vlan outer
protocol_vlan_1 = devices_1.create_protocols('Vlan1')
protocol_vlan_1.protocol_type = 'VLAN'
protocol_vlan_1.parent_link = 'ProtocolEthernet1'
protocol_vlan_1.update()

# create protocols ipv6
protocol_ipv6_1 = devices_1.create_protocols('IPV61')
protocol_ipv6_1.protocol_type = 'IPV6'
protocol_ipv6_1.parent_link = 'Vlan1'
protocol_ipv6_1.update()

# config mac addr
eth_1 = protocol_eth_1.ethernet()
eth_1.update()

eth_1_mac = eth_1.mac()
eth_1_mac.pattern_type = 'SINGLE'
eth_1_mac.update()

eth_1_mac_incr = eth_1_mac.increment()
eth_1_mac_incr.start = '00:10:84:00:00:01'
eth_1_mac_incr.update()

# config ipv6 address
ipv6_1 = protocol_ipv6_1.ipv6()
ipv6_1.update()

ipv6_1_src_addr = ipv6_1.source_address()
ipv6_1_src_addr.pattern_type = 'SINGLE'
ipv6_1_src_addr.single = '2000::6'
ipv6_1_src_addr.update()

ipv6_1_gw_addr = ipv6_1.gateway_address()
ipv6_1_gw_addr.pattern_type = 'SINGLE'
ipv6_1_gw_addr.single = '2000::16'
ipv6_1_gw_addr.update()

#create and config ospfv3 protocol
protocol_ospfv3_1 = devices_1.create_protocols('OSPFV31')
protocol_ospfv3_1.protocol_type = 'OSPFV3'
protocol_ospfv3_1.parent_link = 'IPV61'
protocol_ospfv3_1.update()

ospfv3 = protocol_ospfv3_1.ospfv3()
ospfv3.update()

router_id = ospfv3.router_id()
router_id.single = '11.1.1.1'
router_id.update()

area_id = ospfv3.area_id()
area_id.single = '10.10.10.10'
area_id.update()

network_type = ospfv3.network_type()
network_type.single = 'NATIVE'
network_type.update()

router_priority = ospfv3.router_priority()
router_priority.single = '1'
router_priority.update()

interface_cost = ospfv3.interface_cost()
interface_cost.single = '1'
interface_cost.update()

hello_interval = ospfv3.hello_interval()
hello_interval.single = '10'
hello_interval.update()

router_dead_interval = ospfv3.router_dead_interval()
router_dead_interval.single = '40'
router_dead_interval.update()

retransmit_interval = ospfv3.retransmit_interval()
retransmit_interval.single = '5'
retransmit_interval.update()

#ospfv3 route creation on ospfv3 device
simulated_networks_1 = device_group_east.create_simulated_networks('SimulatedNetworks1')
simulated_networks_1.device_count_per_port = 1
simulated_networks_1.parent_link = 'Device1'
simulated_networks_1.update()

# create 'ospfv3 Route Range' under the simulated_networks_1
networks_1 = simulated_networks_1.create_networks('OSPFV3Networks1')
networks_1.flow_link = 'OSPFV31'
networks_1.network_type = 'OSPFV3_ROUTE_RANGE'
networks_1.update()

#config the ospfv3_route_range_1
ospfv3_route_range_1 = networks_1.ospfv3_route_range()    
ospfv3_route_range_1.update()

ospfv3_route_age = ospfv3_route_range_1.age()
ospfv3_route_age.pattern_type = 'SINGLE'
ospfv3_route_age.single = '67'
ospfv3_route_age.update()

advertise_router_id = ospfv3_route_range_1.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.5'
advertise_router_id.update()

advertise_seq_num = ospfv3_route_range_1.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

#config the ospfv3_router link
ospfv3_router_link_1 = ospfv3_route_range_1.create_ospfv3_router_link('routerlink1')
ospfv3_router_link_1.update()

router_link_type_1 = ospfv3_router_link_1.router_link_type()
router_link_type_1.update()

router_link_type_1.pattern_type = 'SINGLE'
router_link_type_1.single = 'POINT_TO_POINT'
router_link_type_1.update()

interface_id_1 = ospfv3_router_link_1.interface_id()
interface_id_1.update()

interface_id_1.pattern_type = 'SINGLE'
interface_id_1.single = '1000'
interface_id_1.update()

# create 'ospfv3 Route Range' under the simulated_networks_1
networks_3 = simulated_networks_1.create_networks('OSPFV3Networks3')
networks_3.flow_link = 'OSPFV31'
networks_3.network_type = 'OSPFV3_INTER_AREA_PREFIX_RANGE'
networks_3.update()

#config the ospfv3_route_range_1
ospfv3_route_range_3 = networks_3.ospfv3_inter_area_prefix_range()    
ospfv3_route_range_3.update()

ospfv3_route_age = ospfv3_route_range_3.age()
ospfv3_route_age.pattern_type = 'SINGLE'
ospfv3_route_age.single = '67'
ospfv3_route_age.update()

advertise_router_id = ospfv3_route_range_3.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.11'
advertise_router_id.update()

advertise_seq_num = ospfv3_route_range_3.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

# create '' under the simulated_networks_1
networks_1 = simulated_networks_1.create_networks('OSPFV3Networks5')
networks_1.flow_link = 'OSPFV31'
networks_1.network_type = 'OSPFV3_INTRA_AREA_PREFIX_RANGE'
networks_1.update()

#config the ospfv3_route_range_1
ospfv3_route_range_1 = networks_1.ospfv3_intra_area_prefix_range()    
ospfv3_route_range_1.update()

ospfv3_route_age = ospfv3_route_range_1.age()
ospfv3_route_age.pattern_type = 'SINGLE'
ospfv3_route_age.single = '67'
ospfv3_route_age.update()

advertise_router_id = ospfv3_route_range_1.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.13'
advertise_router_id.update()

advertise_seq_num = ospfv3_route_range_1.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

# create 'ospfv3 Route Range' under the simulated_networks_1
networks_1 = simulated_networks_1.create_networks('OSPFV3Networks7')
networks_1.flow_link = 'OSPFV31'
networks_1.network_type = 'OSPFV3_AS_EXTERNAL_PREFIX_RANGE'
networks_1.update()

#config the ospfv3_route_range_1
ospfv3_route_range_1 = networks_1.ospfv3_as_external_prefix_range()    
ospfv3_route_range_1.update()

ospfv3_route_age = ospfv3_route_range_1.age()
ospfv3_route_age.pattern_type = 'SINGLE'
ospfv3_route_age.single = '67'
ospfv3_route_age.update()

advertise_router_id = ospfv3_route_range_1.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.15'
advertise_router_id.update()

advertise_seq_num = ospfv3_route_range_1.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

##########################################################
# ospfv3 Device configuration on port2
device_group_west = config.create_device_groups('WestSideDevicegroup1')
device_group_west.ports = ['Ethernet2']
device_group_west.update()

# create devices: 'Devices 2' under the device_group_west
devices_2 = device_group_west.create_devices('Device2')

# create protocols ethernet
protocol_eth_2 = devices_2.create_protocols('ProtocolEthernet2')
protocol_eth_2.protocol_type = 'ETHERNET'
protocol_eth_2.update()

# create protocols vlan outer
protocol_vlan_3 = devices_2.create_protocols('Vlan2')
protocol_vlan_3.protocol_type = 'VLAN'
protocol_vlan_3.parent_link = 'ProtocolEthernet2'
protocol_vlan_3.update()

# create protocols ipv6
protocol_ipv6_2 = devices_2.create_protocols('IPV62')
protocol_ipv6_2.protocol_type = 'IPV6'
protocol_ipv6_2.parent_link = 'Vlan2'
protocol_ipv6_2.update()

# config mac addr
eth_2 = protocol_eth_2.ethernet()
eth_2.update()

eth_2_mac = eth_1.mac()
eth_2_mac.pattern_type = 'SINGLE'
eth_2_mac.update()

eth_2_mac_incr = eth_2_mac.increment()
eth_2_mac_incr.start = '00:20:94:00:00:02'
eth_2_mac_incr.update()

# config ipv6 address
ipv6_2 = protocol_ipv6_2.ipv6()
ipv6_2.update()

ipv6_2_src_addr = ipv6_2.source_address()
ipv6_2_src_addr.pattern_type = 'SINGLE'
ipv6_2_src_addr.single = '2000::16'
ipv6_2_src_addr.update()

ipv6_2_gw_addr = ipv6_2.gateway_address()
ipv6_2_gw_addr.pattern_type = 'SINGLE'
ipv6_2_gw_addr.single = '2000::6'
ipv6_2_gw_addr.update()

#create and config ospfv3 protocol
protocol_ospfv3_2 = devices_2.create_protocols('OSPFV32')
protocol_ospfv3_2.protocol_type = 'OSPFV3'
protocol_ospfv3_2.parent_link = 'IPV62'
protocol_ospfv3_2.update()

ospfv3 = protocol_ospfv3_2.ospfv3()
ospfv3.update()

router_id = ospfv3.router_id()
router_id.single = '12.1.1.1'
router_id.update()

area_id = ospfv3.area_id()
area_id.single = '10.10.10.10'
area_id.update()

network_type = ospfv3.network_type()
network_type.single = 'NATIVE'
network_type.update()

router_priority = ospfv3.router_priority()
router_priority.single = '0'
router_priority.update()

interface_cost = ospfv3.interface_cost()
interface_cost.single = '1'
interface_cost.update()

hello_interval = ospfv3.hello_interval()
hello_interval.single = '10'
hello_interval.update()

router_dead_interval = ospfv3.router_dead_interval()
router_dead_interval.single = '40'
router_dead_interval.update()

retransmit_interval = ospfv3.retransmit_interval()
retransmit_interval.single = '5'
retransmit_interval.update()

#ospfv3 route creation on ospfv3 device
simulated_networks_2 = device_group_west.create_simulated_networks('SimulatedNetworks2')
simulated_networks_2.device_count_per_port = 1
simulated_networks_2.parent_link = 'Device2'
simulated_networks_2.update()

# create 'ospfv3 Route Range' under the simulated_networks_1
networks_2 = simulated_networks_2.create_networks('OSPFV3Networks2')
networks_2.flow_link = 'OSPFV32'
networks_2.network_type = 'OSPFV3_ROUTE_RANGE'
networks_2.update()

#config the ospfv3_route_range_1
ospfv3_route_range_2 = networks_2.ospfv3_route_range()    
ospfv3_route_range_2.update()

ospfv3_route_age = ospfv3_route_range_2.age()
ospfv3_route_age.pattern_type = 'SINGLE'
ospfv3_route_age.single = '67'
ospfv3_route_age.update()

advertise_router_id = ospfv3_route_range_2.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.7'
advertise_router_id.update()

advertise_seq_num = ospfv3_route_range_2.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

#config the ospfv3_router link
ospfv3_router_link_2 = ospfv3_route_range_2.create_ospfv3_router_link('routerlink2')
ospfv3_router_link_2.update()

router_link_type_2 = ospfv3_router_link_2.router_link_type()
router_link_type_2.update()

router_link_type_2.pattern_type = 'SINGLE'
router_link_type_2.single = 'POINT_TO_POINT'
router_link_type_2.update()

interface_id_2 = ospfv3_router_link_2.interface_id()
interface_id_2.update()

interface_id_2.pattern_type = 'SINGLE'
interface_id_2.single = '2000'
interface_id_2.update()

# create 'ospfv3 Route Range' under the simulated_networks_1
networks_2 = simulated_networks_2.create_networks('OSPFV3Networks4')
networks_2.flow_link = 'OSPFV32'
networks_2.network_type = 'OSPFV3_INTER_AREA_PREFIX_RANGE'
networks_2.update()

#config the ospfv3_route_range_1
ospfv3_route_range_2 = networks_2.ospfv3_inter_area_prefix_range()    
ospfv3_route_range_2.update()

ospfv3_route_age = ospfv3_route_range_2.age()
ospfv3_route_age.pattern_type = 'SINGLE'
ospfv3_route_age.single = '67'
ospfv3_route_age.update()

advertise_router_id = ospfv3_route_range_2.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.21'
advertise_router_id.update()

advertise_seq_num = ospfv3_route_range_2.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

# create '' under the simulated_networks_1
networks_2 = simulated_networks_2.create_networks('OSPFV3Networks6')
networks_2.flow_link = 'OSPFV32'
networks_2.network_type = 'OSPFV3_INTRA_AREA_PREFIX_RANGE'
networks_2.update()

#config the ospfv3_route_range_1
ospfv3_route_range_2 = networks_2.ospfv3_intra_area_prefix_range()    
ospfv3_route_range_2.update()

ospfv3_route_age = ospfv3_route_range_2.age()
ospfv3_route_age.pattern_type = 'SINGLE'
ospfv3_route_age.single = '67'
ospfv3_route_age.update()

advertise_router_id = ospfv3_route_range_2.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.23'
advertise_router_id.update()

advertise_seq_num = ospfv3_route_range_2.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

# create 'ospfv3 Route Range' under the simulated_networks_1
networks_2 = simulated_networks_2.create_networks('OSPFV3Networks8')
networks_2.flow_link = 'OSPFV32'
networks_2.network_type = 'OSPFV3_AS_EXTERNAL_PREFIX_RANGE'
networks_2.update()

#config the ospfv3_route_range_1
ospfv3_route_range_2 = networks_2.ospfv3_as_external_prefix_range()    
ospfv3_route_range_2.update()

ospfv3_route_age = ospfv3_route_range_2.age()
ospfv3_route_age.pattern_type = 'SINGLE'
ospfv3_route_age.single = '67'
ospfv3_route_age.update()

advertise_router_id = ospfv3_route_range_2.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.25'
advertise_router_id.update()

advertise_seq_num = ospfv3_route_range_2.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

#  step 4. start OSPF protocol
print('\n  step 4. start OSPF protocol\n')
ospfv3_control_input1 = config.Ospfv3ControlInput()
ospfv3_control_input1.targets.append('OSPFV31')
ospfv3_control_input1.targets.append('OSPFV32')
ospfv3_control_input1.mode = 'START'
config.ospfv3_control(ospfv3_control_input1)

print('\n  Waiting for 45secs to establish desired state\n')
time.sleep(45)

#   Get the ospfv3 statistics
print('\n  Get the ospfv3 statistics\n')
statistics = session.statistics()

ospfv3_statistics_1 = statistics.ospfv3_statistics('Device1')
ospfv3_statistics_2 = statistics.ospfv3_statistics('Device2')
print(ospfv3_statistics_1._values)
print(ospfv3_statistics_2._values)

ospfv3_state1 = ospfv3_statistics_1._values['adjacency-status']
ospfv3_state2 = ospfv3_statistics_2._values['adjacency-status']

if (ospfv3_state1 == 'FULL'and ospfv3_state2 == 'FULL') :
    print('*' * 40)
    print ("\n Info :OSPF session established successful \n")
    print('*' * 40)
else :
    print ("\n <error> Failed to establish OSPF sessions")
    sys.exit();

# create BOUND streamblock - IPv4 endpoints
device_traffic = config.create_device_traffic('IPV6Stream1')

# ENPOINTS: Devices
device_traffic.encapsulation = "IPV6"
device_traffic.sources = ['OSPFV3Networks7']
device_traffic.destinations = ['OSPFV3Networks8']
device_traffic.bidirectional='true'
device_traffic.update()

#Config Frame Size
frame_length_1 = device_traffic.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '512'
frame_length_1.update()

traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('IPV6Stream1')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

time.sleep(5)

traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('IPV6Stream1')
traffic_control_input1.mode = 'STOP'
config.traffic_control(traffic_control_input1)

#  Get the traffic statistics
print('\n  step 6. Get traffic statistics\n')
statistics = session.statistics()
print('%s \n' % statistics._values)
traffic_statistics_1 = statistics.device_traffic('IPV6Stream1')
print('%s \n' % traffic_statistics_1._values)

tx_frames = traffic_statistics_1._values['tx-frames']
rx_frames = traffic_statistics_1._values['rx-frames']

if (tx_frames == rx_frames):
    print('*' * 40)
    print ("\n Info: Traffic is transmitted successfully \n")
    print('*' * 40)
else :
    print ("\n <error> Traffic is not transmitted successfully")
    sys.exit();

#  stop the ospfv3 protocol
print('\n  stop ospfv3 protocol\n')
ospfv3_control_input1 = config.Ospfv3ControlInput()
ospfv3_control_input1.mode = 'STOP'
config.ospfv3_control(ospfv3_control_input1)

port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

session.delete()

print ("COMPLETED................")
