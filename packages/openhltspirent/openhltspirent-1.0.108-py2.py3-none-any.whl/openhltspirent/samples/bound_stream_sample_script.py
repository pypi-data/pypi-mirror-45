# test stpes:

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
    print("######## Deleted existing session with name %s ######### \n" % sessionname)
except:
    print("######## There is no session exist with name %s ######## \n" % sessionname)

# create session : "SampleTest"
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

print('\n  step 2. create devices under the port1, protocol stack: eth/vlan/vlan/ipv4.\n')
device_group_east_1 = config.create_device_groups('EastSideDevicegroup1')
device_group_east_1.ports = ['Ethernet1']
device_group_east_1.update()

# create devices: 'Devices 1' under the device_group_east
devices_1 = device_group_east_1.create_devices('Device1')

# set device count
devices_1.device_count_per_port = 2
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

# config mac addr with increment modifier
eth_1 = protocol_eth_1.ethernet()
eth_1.update()

eth_1_mac = eth_1.mac()
eth_1_mac.pattern_type = 'INCREMENT'
eth_1_mac.update()

eth_1_mac_incr = eth_1_mac.increment()
eth_1_mac_incr.start = '00:10:94:00:00:01'
eth_1_mac_incr.step = '00:00:00:00:00:01'
eth_1_mac_incr.update()

# config vlan outer
vlan_1 = protocol_vlan_1.vlan()
vlan_1.update()

vlan_id_1 = vlan_1.id()
vlan_id_1.pattern_type = 'INCREMENT'
vlan_id_1.update()

vlan_id_1_incr = vlan_id_1.increment()
vlan_id_1_incr.start = '100'
vlan_id_1_incr.step = '1'
vlan_id_1_incr.update()

vlan_pri_1 = vlan_1.priority()
vlan_pri_1.pattern_type = 'SINGLE'
vlan_pri_1.single = '7'
vlan_pri_1.update()

# config vlan inner
vlan_2 = protocol_vlan_2.vlan()
vlan_2.update()

vlan_id_2 = vlan_2.id()
vlan_id_2.pattern_type = 'INCREMENT'
vlan_id_2.update()

vlan_id_incr_2 = vlan_id_2.increment()
vlan_id_incr_2.start = '200'
vlan_id_incr_2.step = '2'
vlan_id_incr_2.update()

vlan_pri_2 = vlan_2.priority()
vlan_pri_2.pattern_type = 'SINGLE'
vlan_pri_2.single = '7'
vlan_pri_2.update()

# config ipv4 address
ipv4_1 = protocol_ipv4_1.ipv4()
ipv4_1.update()

#ipv4_1.source_address = '192.85.1.3'
ipv4_1_src_addr = ipv4_1.source_address()
ipv4_1_src_addr.pattern_type = 'SINGLE'
ipv4_1_src_addr.single = '192.85.1.3'
ipv4_1_src_addr.update()

#ipv4_1.gateway_address = '192.85.1.1'
ipv4_1_gw_addr = ipv4_1.gateway_address()
ipv4_1_gw_addr.pattern_type = 'SINGLE'
ipv4_1_gw_addr.single = '192.85.1.13'
ipv4_1_gw_addr.update()

# get ipv4 source address value
print('\n  IPV4 1 source address : %s \n' % ipv4_1_src_addr.single)

#  step 3. create two devices under the port2, protocol stack: eth/vlan/vlan/ipv4/bgpv4. And add BGP routes
print('\n  step 3. create two devices under the port2, protocol stack: eth/vlan/vlan/ipv4.\n')

# config device groups 'West Side - Device group 1' unde the port 'Ethernet - 002'
device_group_west_1 = config.create_device_groups('WestSideDevicegroup1')
device_group_west_1.ports = ['Ethernet2']
device_group_west_1.update()

# create 'Device 2' under the device_group_west 
devices_2 = device_group_west_1.create_devices('Device2')

# set the device count
devices_2.device_count_per_port = 2
devices_2.update()

# create protocol ethernet
protocol_eth_2 = devices_2.create_protocols('Ethernet2')
protocol_eth_2.protocol_type = 'ETHERNET'
protocol_eth_2.update()

# create protocol vlan outer
protocol_vlan_3 = devices_2.create_protocols('Vlan3')
protocol_vlan_3.protocol_type = 'VLAN'
protocol_vlan_3.parent_link = 'Ethernet2'
protocol_vlan_3.update()

# create protocol vlan inner
protocol_vlan_4 = devices_2.create_protocols('Vlan4')
protocol_vlan_4.protocol_type = 'VLAN'
protocol_vlan_4.parent_link = 'Vlan3'
protocol_vlan_4.update()

# create protocol IPv4
protocol_ipv4_2 = devices_2.create_protocols('IPV42')
protocol_ipv4_2.protocol_type = 'IPV4'
protocol_ipv4_2.parent_link = 'Vlan4'
protocol_ipv4_2.update()

# # config mac addr
eth_2 = protocol_eth_2.ethernet()
eth_2.update()

eth_2_mac = eth_2.mac()
eth_2_mac.pattern_type = 'INCREMENT'
eth_2_mac.update()

eth_2_mac_incr = eth_2_mac.increment()
eth_2_mac_incr.start = '00:10:94:00:00:10'
eth_2_mac_incr.step = '00:00:00:00:00:01'
eth_2_mac_incr.update()


# config vlan outer
vlan_3 = protocol_vlan_3.vlan()
vlan_3.update()

vlan_id_3 = vlan_3.id()
vlan_id_3.pattern_type = 'INCREMENT'
vlan_id_3.update()

vlan_id_3_incr = vlan_id_3.increment()
vlan_id_3_incr.start = '100'
vlan_id_3_incr.step = '1'
vlan_id_3_incr.update()

vlan_pri_3 = vlan_3.priority()
vlan_pri_3.pattern_type = 'SINGLE'
vlan_pri_3.single = '7'
vlan_pri_3.update()


# config vlan inner
vlan_4 = protocol_vlan_4.vlan()
vlan_4.update()

vlan_id_4 = vlan_4.id()
vlan_id_4.pattern_type = 'INCREMENT'
vlan_id_4.update()

vlan_id_incr_4 = vlan_id_4.increment()
vlan_id_incr_4.start = '200'
vlan_id_incr_4.step = '2'
vlan_id_incr_4.update()

vlan_pri_4 = vlan_4.priority()
vlan_pri_4.pattern_type = 'SINGLE'
vlan_pri_4.single = '7'
vlan_pri_4.update()

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


print('\n  step 4. create devices under the port1, protocol stack: eth/vlan/vlan/ipv6.\n')
device_group_east_2 = config.create_device_groups('EastSideDevicegroup2')
device_group_east_2.ports = ['Ethernet1']
device_group_east_2.update()

# create devices: 'Devices 1' under the device_group_east
devices_3 = device_group_east_2.create_devices('Device3')

# set device count
devices_3.device_count_per_port = 2
devices_3.update()

# create protocols ethernet
protocol_eth_3 = devices_3.create_protocols('Ethernet3')
protocol_eth_3.protocol_type = 'ETHERNET'
protocol_eth_3.update()

# create protocols vlan outer
protocol_vlan_5 = devices_3.create_protocols('Vlan5')
protocol_vlan_5.protocol_type = 'VLAN'
protocol_vlan_5.parent_link = 'Ethernet3'
protocol_vlan_5.update()

# create protocols vlan inner
protocol_vlan_6 = devices_3.create_protocols('Vlan6')
protocol_vlan_6.protocol_type = 'VLAN'
protocol_vlan_6.parent_link = 'Vlan5'
protocol_vlan_6.update()

# create protocols IPv6
protocol_ipv6_1 = devices_3.create_protocols('IPV61')
protocol_ipv6_1.protocol_type = 'IPV6'
protocol_ipv6_1.parent_link = 'Vlan6'
protocol_ipv6_1.update()

# config mac addr with increment modifier
eth_3 = protocol_eth_3.ethernet()
eth_3.update()

eth_3_mac = eth_3.mac()
eth_3_mac.pattern_type = 'INCREMENT'
eth_3_mac.update()

eth_3_mac_incr = eth_3_mac.increment()
eth_3_mac_incr.start = '00:10:94:00:00:31'
eth_3_mac_incr.step = '00:00:00:00:00:01'
eth_3_mac_incr.update()

# config vlan outer
vlan_5 = protocol_vlan_5.vlan()
vlan_5.update()

vlan_id_5 = vlan_5.id()
vlan_id_5.pattern_type = 'INCREMENT'
vlan_id_5.update()

vlan_id_5_incr = vlan_id_5.increment()
vlan_id_5_incr.start = '100'
vlan_id_5_incr.step = '1'
vlan_id_5_incr.update()

vlan_pri_5 = vlan_5.priority()
vlan_pri_5.pattern_type = 'SINGLE'
vlan_pri_5.single = '7'
vlan_pri_5.update()

# config vlan inner
vlan_6 = protocol_vlan_6.vlan()
vlan_6.update()

vlan_id_6 = vlan_6.id()
vlan_id_6.pattern_type = 'INCREMENT'
vlan_id_6.update()

vlan_id_incr_6 = vlan_id_6.increment()
vlan_id_incr_6.start = '200'
vlan_id_incr_6.step = '2'
vlan_id_incr_6.update()

vlan_pri_6 = vlan_6.priority()
vlan_pri_6.pattern_type = 'SINGLE'
vlan_pri_6.single = '7'
vlan_pri_6.update()

# config ipv6 address
ipv6_1 = protocol_ipv6_1.ipv6()
ipv6_1.update()

#ipv6_1.source_address = '2000::10'
ipv6_1_src_addr = ipv6_1.source_address()
ipv6_1_src_addr.pattern_type = 'SINGLE'
ipv6_1_src_addr.single = '2000::10'
ipv6_1_src_addr.update()

#ipv6_1.gateway_address = '2000::1'
ipv6_1_gw_addr = ipv6_1.gateway_address()
ipv6_1_gw_addr.pattern_type = 'SINGLE'
ipv6_1_gw_addr.single = '2000::1'
ipv6_1_gw_addr.update()

# get ipv6 source address value
print('\n  IPV6 1 source address : %s \n' % ipv6_1_src_addr.single)

print('\n  step 5. create two devices under the port2, protocol stack: eth/vlan/vlan/ipv6.\n')

# config device groups 'West Side - Device group 1' unde the port 'Ethernet - 002'
device_group_west_2 = config.create_device_groups('WestSideDevicegroup2')
device_group_west_2.ports = ['Ethernet2']
device_group_west_2.update()

devices_4 = device_group_west_2.create_devices('Device4')

# set the device count
devices_4.device_count_per_port = 2
devices_4.update()

# create protocol ethernet
protocol_eth_4 = devices_4.create_protocols('Ethernet4')
protocol_eth_4.protocol_type = 'ETHERNET'
protocol_eth_4.update()

# create protocol vlan outer
protocol_vlan_7 = devices_4.create_protocols('Vlan7')
protocol_vlan_7.protocol_type = 'VLAN'
protocol_vlan_7.parent_link = 'Ethernet4'
protocol_vlan_7.update()

# create protocol vlan inner
protocol_vlan_8 = devices_4.create_protocols('Vlan8')
protocol_vlan_8.protocol_type = 'VLAN'
protocol_vlan_8.parent_link = 'Vlan7'
protocol_vlan_8.update()

# create protocol IPv6
protocol_ipv6_2 = devices_4.create_protocols('IPV62')
protocol_ipv6_2.protocol_type = 'IPV6'
protocol_ipv6_2.parent_link = 'Vlan8'
protocol_ipv6_2.update()

# # config mac addr
eth_4 = protocol_eth_4.ethernet()
eth_4.update()

eth_4_mac = eth_4.mac()
eth_4_mac.pattern_type = 'INCREMENT'
eth_4_mac.update()

eth_4_mac_incr = eth_4_mac.increment()
eth_4_mac_incr.start = '00:10:94:00:00:40'
eth_4_mac_incr.step = '00:00:00:00:00:01'
eth_4_mac_incr.update()


# config vlan outer
vlan_7 = protocol_vlan_7.vlan()
vlan_7.update()

vlan_id_7 = vlan_7.id()
vlan_id_7.pattern_type = 'INCREMENT'
vlan_id_7.update()

vlan_id_7_incr = vlan_id_7.increment()
vlan_id_7_incr.start = '100'
vlan_id_7_incr.step = '1'
vlan_id_7_incr.update()

vlan_pri_7 = vlan_7.priority()
vlan_pri_7.pattern_type = 'SINGLE'
vlan_pri_7.single = '7'
vlan_pri_7.update()


# config vlan inner
vlan_8 = protocol_vlan_8.vlan()
vlan_8.update()

vlan_id_8 = vlan_8.id()
vlan_id_8.pattern_type = 'INCREMENT'
vlan_id_8.update()

vlan_id_incr_8 = vlan_id_8.increment()
vlan_id_incr_8.start = '200'
vlan_id_incr_8.step = '2'
vlan_id_incr_8.update()

vlan_pri_8 = vlan_8.priority()
vlan_pri_8.pattern_type = 'SINGLE'
vlan_pri_8.single = '7'
vlan_pri_8.update()

# config ipv4 address
ipv6_2 = protocol_ipv6_2.ipv6()
ipv6_2.update()

ipv6_2_src_addr = ipv6_2.source_address()
ipv6_2_src_addr.pattern_type = 'SINGLE'
ipv6_2_src_addr.single = '2000::10'
ipv6_2_src_addr.update()


ipv6_2_gw_addr = ipv6_2.gateway_address()
ipv6_2_gw_addr.pattern_type = 'SINGLE'
ipv6_2_gw_addr.single = '2000::1'
ipv6_2_gw_addr.update()


# create BOUND streamblock - IPv4 endpoints
device_traffic_1 = config.create_device_traffic('IPV4Stream1')

# ENPOINTS: Devices
device_traffic_1.encapsulation = "IPV4"
device_traffic_1.sources = ['IPV41']
device_traffic_1.destinations = ['IPV42']
device_traffic_1.bidirectional='true'
device_traffic_1.update()

#Config Frame Size
frame_length_1 = device_traffic_1.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '512'
frame_length_1.update()


# create BOUND streamblock - IPv4 endpoints
device_traffic_2 = config.create_device_traffic('IPV6Stream1')

# ENPOINTS: Devices
device_traffic_2.encapsulation = "IPV6"
device_traffic_2.sources = ['Device3']
device_traffic_2.destinations = ['Device4']
device_traffic_2.bidirectional='true'
device_traffic_2.update()

#Config Frame Size
frame_length_2 = device_traffic_2.frame_length()
frame_length_2.length_type = 'FIXED'
frame_length_2.fixed = '256'
frame_length_2.update()


traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('IPV4Stream1')
traffic_control_input1.targets.append('IPV6Stream1')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

time.sleep(5)

traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('IPV4Stream1')
traffic_control_input1.targets.append('IPV6Stream1')
traffic_control_input1.mode = 'STOP'
config.traffic_control(traffic_control_input1)


#  Get the traffic statistics
print('\n  step 6. Get traffic statistics\n')
statistics = session.statistics()
print('%s \n' % statistics._values)
traffic_statistics_1 = statistics.device_traffic('IPV4Stream1')
print('%s \n' % traffic_statistics_1._values)
traffic_statistics_2 =  statistics.device_traffic('IPV6Stream1')
print('%s \n' % traffic_statistics_2._values)

#disconnect ports
port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

session.delete()

