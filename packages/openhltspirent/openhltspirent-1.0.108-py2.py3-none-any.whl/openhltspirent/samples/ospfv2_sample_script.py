##Test Steps
    #Step 1:  Create a session and connect to two back to back stc ports
    #Step 2:  Configue ospfv2 devices on each port
    #Step 3:  Configure ospfv2 routes one each ospf device
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

#Commandline arguments
serverip=sys.argv[1]
chassisip=sys.argv[2]
sessionname=sys.argv[3]
portnumber=sys.argv[4]

print("ohtweb server ip", serverip)
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
port1.location = chassisip + r'/1/1'
port1.update()

port2 = config.create_ports('Ethernet2')
port2.location = chassisip + r'/1/2' 
port2.update()

port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'CONNECT'
config.port_control(port_control_input)

#  step 2. create two devices under the port1, protocol stack: eth/vlan/vlan/ipv4/ospfv2. 
print('\n  step 2. create two devices under the port1, protocol stack: eth/vlan/vlan/ipv4/ospfv2.\n')
# create device groups: 'East Side - Device group 1' under the port 'Ethernet - 001'
device_group_east = config.create_device_groups('EastSideDevicegroup1')
device_group_east.ports = ['Ethernet1']
device_group_east.update()

# create devices: 'Devices 1' under the device_group_east
devices_1 = device_group_east.create_devices('Device1')

#set device count
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

ipv4_1_src_addr = ipv4_1.source_address()
ipv4_1_src_addr.pattern_type = 'SINGLE'
ipv4_1_src_addr.single = '192.85.1.3'
ipv4_1_src_addr.update()

ipv4_1_gw_addr = ipv4_1.gateway_address()
ipv4_1_gw_addr.pattern_type = 'SINGLE'
ipv4_1_gw_addr.single = '192.85.1.13'
ipv4_1_gw_addr.update()

ipv4_1_prefix_addr = ipv4_1.prefix()
ipv4_1_prefix_addr.pattern_type = 'SINGLE'
ipv4_1_prefix_addr.single = '19'
ipv4_1_prefix_addr.update()

#create and config OSPFv2 protocol
protocol_ospfv2_1 = devices_1.create_protocols('OSPFV21')
protocol_ospfv2_1.protocol_type = 'OSPFV2'
protocol_ospfv2_1.parent_link = 'IPV41'
protocol_ospfv2_1.update()

ospfv2 = protocol_ospfv2_1.ospfv2()
ospfv2.update()

router_id = ospfv2.router_id()
router_id.single = '11.1.1.1'
router_id.update()

area_id = ospfv2.area_id()
area_id.single = '10.10.10.10'
area_id.update()

network_type = ospfv2.network_type()
network_type.single = 'NATIVE'
network_type.update()

router_priority = ospfv2.router_priority()
router_priority.single = '1'
router_priority.update()

interface_cost = ospfv2.interface_cost()
interface_cost.single = '1'
interface_cost.update()

hello_interval = ospfv2.hello_interval()
hello_interval.single = '10'
hello_interval.update()

router_dead_interval = ospfv2.router_dead_interval()
router_dead_interval.single = '40'
router_dead_interval.update()

retransmit_interval = ospfv2.retransmit_interval()
retransmit_interval.single = '5'
retransmit_interval.update()

#OSPFV2 route creation on OSPFV2 device
simulated_networks_1 = device_group_east.create_simulated_networks('SimulatedNetworks1')
simulated_networks_1.device_count_per_port = 1
simulated_networks_1.parent_link = 'Device1'
simulated_networks_1.update()

# create 'OSPFV2 Route Range' under the simulated_networks_1
networks_1 = simulated_networks_1.create_networks('OSPFV2Networks1')
networks_1.flow_link = 'OSPFV21'
networks_1.network_type = 'OSPFV2_ROUTE_RANGE'
networks_1.update()

#config the ospfv2_route_range_1
ospfv2_route_range_1 = networks_1.ospfv2_route_range()
ospfv2_route_range_1.update()

advertise_router_id = ospfv2_route_range_1.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.0'
advertise_router_id.update()

ospfv2_route_age = ospfv2_route_range_1.age()
ospfv2_route_age.pattern_type = 'SINGLE'
ospfv2_route_age.single = '67'
ospfv2_route_age.update()

advertise_seq_num = ospfv2_route_range_1.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

#config the ospfv2_router link
ospfv2_router_link_1 = ospfv2_route_range_1.create_ospfv2_router_link('routerlink1')
ospfv2_router_link_1.update()

router_link_type_1 = ospfv2_router_link_1.router_link_type()
router_link_type_1.update()

router_link_type_1.pattern_type = 'SINGLE'
router_link_type_1.single = 'POINT_TO_POINT'
router_link_type_1.update()

router_link_id_1 = ospfv2_router_link_1.router_link_id()
router_link_id_1.update()

router_link_id_1.pattern_type = 'SINGLE'
router_link_id_1.single = '11.1.1.1'
router_link_id_1.update()

# create 'OSPFV2 summary Range' under the simulated_networks_1
networks_2 = simulated_networks_1.create_networks('OSPFV2Networks1_2')
networks_2.flow_link = 'OSPFV21'
networks_2.network_type = 'OSPFV2_SUMMARY_RANGE'
networks_2.update()

#config the ospfv2_sumamry_range_1
ospfv2_summary_range_1 = networks_2.ospfv2_summary_range()
ospfv2_summary_range_1.update()

advertise_router_id = ospfv2_summary_range_1.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.2.0'
advertise_router_id.update()

ospfv2_sumamry_age = ospfv2_summary_range_1.age()
ospfv2_sumamry_age.pattern_type = 'SINGLE'
ospfv2_sumamry_age.single = '67'
ospfv2_sumamry_age.update()

advertise_seq_num = ospfv2_summary_range_1.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

# create 'OSPFV2 external Range' under the simulated_networks_1
networks_3 = simulated_networks_1.create_networks('OSPFV2Networks1_3')
networks_3.flow_link = 'OSPFV21'
networks_3.network_type = 'OSPFV2_EXTERNAL_RANGE'
networks_3.update()

#config the ospfv2_external_range_1
ospfv2_external_range_1 = networks_3.ospfv2_external_range()
ospfv2_external_range_1.update()

advertise_router_id = ospfv2_external_range_1.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.3.0'
advertise_router_id.update()

ospfv2_sumamry_age = ospfv2_external_range_1.age()
ospfv2_sumamry_age.pattern_type = 'SINGLE'
ospfv2_sumamry_age.single = '67'
ospfv2_sumamry_age.update()

advertise_seq_num = ospfv2_external_range_1.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

# create 'OSPFV2 nssa Range' under the simulated_networks_1
networks_4 = simulated_networks_1.create_networks('OSPFV2Networks1_4')
networks_4.flow_link = 'OSPFV21'
networks_4.network_type = 'OSPFV2_NSSA_RANGE'
networks_4.update()

#config the ospfv2_nssa_range_1
ospfv2_nssa_range_1 = networks_4.ospfv2_nssa_range()
ospfv2_nssa_range_1.update()

advertise_router_id = ospfv2_nssa_range_1.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.4.0'
advertise_router_id.update()

ospfv2_sumamry_age = ospfv2_nssa_range_1.age()
ospfv2_sumamry_age.pattern_type = 'SINGLE'
ospfv2_sumamry_age.single = '67'
ospfv2_sumamry_age.update()

advertise_seq_num = ospfv2_nssa_range_1.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

##########################################################
# OSPFv2 Device configuration on port2
device_group_west = config.create_device_groups('WestSideDevicegroup1')
device_group_west.ports = ['Ethernet2']
device_group_west.update()

# create devices: 'Devices 2' under the device_group_west
devices_2 = device_group_west.create_devices('Device2')

#set device count
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
protocol_ipv4_2 = devices_2.create_protocols('WestIPV41')
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

ipv4_2_src_addr = ipv4_2.source_address()
ipv4_2_src_addr.pattern_type = 'SINGLE'
ipv4_2_src_addr.single = '192.85.1.13'
ipv4_2_src_addr.update()

ipv4_2_gw_addr = ipv4_2.gateway_address()
ipv4_2_gw_addr.pattern_type = 'SINGLE'
ipv4_2_gw_addr.single = '192.85.1.3'
ipv4_2_gw_addr.update()

#create and config OSPFv2 protocol
protocol_ospfv2_2 = devices_2.create_protocols('OSPFV22')
protocol_ospfv2_2.protocol_type = 'OSPFV2'
protocol_ospfv2_2.parent_link = 'WestIPV41'
protocol_ospfv2_2.update()

ospfv2 = protocol_ospfv2_2.ospfv2()
ospfv2.update()

router_id = ospfv2.router_id()
router_id.single = '12.1.1.1'
router_id.update()

area_id = ospfv2.area_id()
area_id.single = '10.10.10.10'
area_id.update()

network_type = ospfv2.network_type()
network_type.single = 'NATIVE'
network_type.update()

router_priority = ospfv2.router_priority()
router_priority.single = '0'
router_priority.update()

interface_cost = ospfv2.interface_cost()
interface_cost.single = '1'
interface_cost.update()

hello_interval = ospfv2.hello_interval()
hello_interval.single = '10'
hello_interval.update()

router_dead_interval = ospfv2.router_dead_interval()
router_dead_interval.single = '40'
router_dead_interval.update()

retransmit_interval = ospfv2.retransmit_interval()
retransmit_interval.single = '5'
retransmit_interval.update()

#OSPFV2 route creation on OSPFV2 device
simulated_networks_2 = device_group_west.create_simulated_networks('SimulatedNetworks2')
simulated_networks_2.device_count_per_port = 1
simulated_networks_2.parent_link = 'Device2'
simulated_networks_2.update()

# create 'OSPFV2 Route Range' under the simulated_networks_1
networks_2 = simulated_networks_2.create_networks('OSPFV2Networks2')
networks_2.flow_link = 'OSPFV22'
networks_2.network_type = 'OSPFV2_ROUTE_RANGE'
networks_2.update()

#config the ospfv2_route_range_2
ospfv2_route_range_2 = networks_2.ospfv2_route_range()
ospfv2_route_range_2.update()

advertise_router_id = ospfv2_route_range_2.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.1.10'
advertise_router_id.update()

ospfv2_route_age = ospfv2_route_range_2.age()
ospfv2_route_age.pattern_type = 'SINGLE'
ospfv2_route_age.single = '67'
ospfv2_route_age.update()

#config the ospfv2_router link
ospfv2_router_link_2 = ospfv2_route_range_2.create_ospfv2_router_link('routerlink2')
ospfv2_router_link_2.update()

router_link_type_2 = ospfv2_router_link_2.router_link_type()

router_link_type_2.pattern_type = 'SINGLE'
router_link_type_2.single = 'POINT_TO_POINT'
router_link_type_2.update()

router_link_id_2 = ospfv2_router_link_2.router_link_id()

router_link_id_2.pattern_type = 'SINGLE'
router_link_id_2.single = '11.1.1.12'
router_link_id_2.update()

# create 'OSPFV2 summary Range' under the simulated_networks_1
networks_21 = simulated_networks_2.create_networks('OSPFV2Networks2_2')
networks_21.flow_link = 'OSPFV22'
networks_21.network_type = 'OSPFV2_SUMMARY_RANGE'
networks_21.update()

#config the ospfv2_sumamry_range_1
ospfv2_summary_range_2 = networks_21.ospfv2_summary_range()
ospfv2_summary_range_2.update()

advertise_router_id = ospfv2_summary_range_2.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.2.10'
advertise_router_id.update()

ospfv2_sumamry_age = ospfv2_summary_range_2.age()
ospfv2_sumamry_age.pattern_type = 'SINGLE'
ospfv2_sumamry_age.single = '67'
ospfv2_sumamry_age.update()

# create 'OSPFV2 external Range' under the simulated_networks_1
networks_31 = simulated_networks_2.create_networks('OSPFV2Networks2_3')
networks_31.flow_link = 'OSPFV22'
networks_31.network_type = 'OSPFV2_EXTERNAL_RANGE'
networks_31.update()

#config the ospfv2_external_range_1
ospfv2_external_range_2 = networks_31.ospfv2_external_range()
ospfv2_external_range_2.update()

advertise_router_id = ospfv2_external_range_2.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.3.10'
advertise_router_id.update()

ospfv2_sumamry_age = ospfv2_external_range_2.age()
ospfv2_sumamry_age.pattern_type = 'SINGLE'
ospfv2_sumamry_age.single = '67'
ospfv2_sumamry_age.update()

advertise_seq_num = ospfv2_external_range_2.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

# create 'OSPFV2 nssa Range' under the simulated_networks_1
networks_41 = simulated_networks_2.create_networks('OSPFV2Networks2_4')
networks_41.flow_link = 'OSPFV22'
networks_41.network_type = 'OSPFV2_NSSA_RANGE'
networks_41.update()

#config the ospfv2_nssa_range_1
ospfv2_nssa_range_2 = networks_41.ospfv2_nssa_range()
ospfv2_nssa_range_2.update()

advertise_router_id = ospfv2_nssa_range_2.advertise_router_id()
advertise_router_id.pattern_type = 'SINGLE'
advertise_router_id.single = '192.0.4.10'
advertise_router_id.update()

ospfv2_sumamry_age = ospfv2_nssa_range_2.age()
ospfv2_sumamry_age.pattern_type = 'SINGLE'
ospfv2_sumamry_age.single = '67'
ospfv2_sumamry_age.update()

advertise_seq_num = ospfv2_nssa_range_2.sequence_number()
advertise_seq_num.pattern_type = 'SINGLE'
advertise_seq_num.single = '80000089'
advertise_seq_num.update()

print('\n  step 4. start OSPF protocol\n')
ospfv2_control_input1 = config.Ospfv2ControlInput()
ospfv2_control_input1.mode = 'START'
config.ospfv2_control(ospfv2_control_input1)


time.sleep(45)

#  step 5. Get the OSPF statistics
print('\n  step 5. Get the OSPF statistics\n')
statistics = session.statistics()
print('%s \n' % statistics._values)
ospfv2_statistics_1 = statistics.ospfv2_statistics('Device1')
ospfv2_statistics_2 = statistics.ospfv2_statistics('Device2')
print(ospfv2_statistics_1._values)
print(ospfv2_statistics_2._values)

ospfv2_state1 = ospfv2_statistics_1._values['adjacency-status']
ospfv2_state2 = ospfv2_statistics_2._values['adjacency-status']

if (ospfv2_state1 == 'FULL'and ospfv2_state2 == 'FULL') :
    print('*' * 40)
    print ("\n Info :OSPF session established successful \n")
    print('*' * 40)
else :
    print ("\n <error> Failed to establish OSPF sessions")
    #sys.exit();

# create BOUND streamblock - IPv4 endpoints
device_traffic = config.create_device_traffic('IPV4Stream1')

# ENPOINTS: Devices
device_traffic.encapsulation = "IPV4"
device_traffic.sources = ['OSPFV2Networks1_2']
device_traffic.destinations = ['OSPFV2Networks2_2']
device_traffic.bidirectional='true'
device_traffic.update()

#Config Frame Size
frame_length_1 = device_traffic.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '512'
frame_length_1.update()

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
print('\n  step 6. Get traffic statistics\n')
statistics = session.statistics()
print('%s \n' % statistics._values)
traffic_statistics_1 = statistics.device_traffic('IPV4Stream1')
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

#  stop the ospfv2 protocol
print('\n  stop ospfv2 protocol\n')
ospfv2_control_input1 = config.Ospfv2ControlInput()
ospfv2_control_input1.targets.append('OSPFV21')
ospfv2_control_input1.targets.append('OSPFV22')
ospfv2_control_input1.mode = 'STOP'
config.ospfv2_control(ospfv2_control_input1)
    
#disconnect ports
port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)
session.delete()

print ("COMPLETED................")
