###Test Steps
    #Step 1:  Create a session and connect to two back to back stc ports
    #Step 2:  Configue bgp devices with bfd on each port
    #Step 3:  Configure bgp routes one each bgp device
    #Step 4:  Configure traffic group between two bgp devices
    #Step 5:  Save the configuration as an XML file
    #Step 6:  Start the bgp devices
    #Step 7:  Start the traffic
    #Step 8:  Validate the bgp stats
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

# connect openhltest server
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

print('\n  step 2. create devices under the port1, protocol stack: eth/vlan/ipv6/bgpv6.\n')
device_group_east_1 = config.create_device_groups('EastSideDevicegroup1')
device_group_east_1.ports = ['Ethernet1']
device_group_east_1.update()

# create devices: 'Devices 1' under the device_group_east
devices_1 = device_group_east_1.create_devices('Device1')

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

# create protocols IPv4
protocol_ipv6_1 = devices_1.create_protocols('IPV61')
protocol_ipv6_1.protocol_type = 'IPV6'
protocol_ipv6_1.parent_link = 'Vlan1'
protocol_ipv6_1.update()

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

# config ipv6 address
ipv6_1 = protocol_ipv6_1.ipv6()
ipv6_1.update()

#ipv6_1.source_address = '192.85.1.3'
ipv6_1_src_addr = ipv6_1.source_address()
ipv6_1_src_addr.pattern_type = 'SINGLE'
ipv6_1_src_addr.single = '2000::1'
ipv6_1_src_addr.update()

#ipv6_1.gateway_address = '192.85.1.1'
ipv6_1_gw_addr = ipv6_1.gateway_address()
ipv6_1_gw_addr.pattern_type = 'SINGLE'
ipv6_1_gw_addr.single = '2000::11'
ipv6_1_gw_addr.update()

#create and config BFDv6 protocol
protocol_bfdv6_1 = devices_1.create_protocols('BFDV61')
protocol_bfdv6_1.protocol_type = 'BFDV6'
protocol_bfdv6_1.parent_link = 'IPV61'
protocol_bfdv6_1.update()

bfdv6_1 = protocol_bfdv6_1.bfdv6()
bfdv6_1.update()

transmit_interval = bfdv6_1.transmit_interval()
transmit_interval.pattern_type = 'SINGLE'
transmit_interval.single = '20'
transmit_interval.update()

receive_interval = bfdv6_1.receive_interval()
receive_interval.pattern_type = 'SINGLE'
receive_interval.single = '30'
receive_interval.update()

echo_receive_interval = bfdv6_1.echo_receive_interval()
echo_receive_interval.pattern_type = 'SINGLE'
echo_receive_interval.single = '40'
echo_receive_interval.update()

#create and config BGPv4 protocol
protocol_bgp_1 = devices_1.create_protocols('BGPV61')
protocol_bgp_1.protocol_type = 'BGPV6'
protocol_bgp_1.parent_link = 'IPV61'
protocol_bgp_1.update()

bgpv6_1 = protocol_bgp_1.bgpv6()
bgpv6_1.update()

dut_ipv6_address_1 = bgpv6_1.dut_ipv6_address()
dut_ipv6_address_1.pattern_type = 'SINGLE'
dut_ipv6_address_1.single = '2000::11'
dut_ipv6_address_1.update()

hold_time_interval_1 = bgpv6_1.hold_time_interval()
hold_time_interval_1.pattern_type = 'SINGLE'
hold_time_interval_1.single = '100'
hold_time_interval_1.update()

keep_alive_interval_1 = bgpv6_1.keep_alive_interval()
keep_alive_interval_1.pattern_type = 'SINGLE'
keep_alive_interval_1.single = '50'
keep_alive_interval_1.update()

as_number_2_byte_1 = bgpv6_1.create_as_number_2_byte()
as_number_1 = as_number_2_byte_1.as_number()
as_number_1.pattern_type = 'SINGLE'
as_number_1.single = '20'
as_number_1.update()

dut_as_number_1 = as_number_2_byte_1.dut_as_number()
dut_as_number_1.pdattern_type = 'SINGLE'
dut_as_number_1.single = '10'
dut_as_number_1.update()

# create simulated_networks under the device_group_east
simulated_networks_1 = device_group_east_1.create_simulated_networks('SimulatedNetworks1')
simulated_networks_1.device_count_per_port = 1
simulated_networks_1.parent_link = 'Device1'
simulated_networks_1.update()

# create 'BGPV6 Route Range' under the simulated_networks_1
networks_1 = simulated_networks_1.create_networks('BGPV6Networks1')
networks_1.flow_link = 'BGPV61'
networks_1.network_type = 'BGPV6_ROUTE_RANGE'
networks_1.update()

#config the bgpv6_route_range_1
bgpv6_route_range_1 = networks_1.bgpv6_route_range()
bgpv6_route_range_1.update()

address_1 = bgpv6_route_range_1.address()
address_1.pattern_type = 'SINGLE'
address_1.single = '3000::4'
address_1.update()

prefix_length_1 = bgpv6_route_range_1.prefix_length()
prefix_length_1.pattern_type = 'SINGLE'
prefix_length_1.single = '64'
prefix_length_1.update()

as_path_1 = bgpv6_route_range_1.as_path()
as_path_1.pattern_type = 'SINGLE'
as_path_1.single = '20'
as_path_1.update()

next_hop_address_1 = bgpv6_route_range_1.next_hop_address()
next_hop_address_1.pattern_type = 'SINGLE'
next_hop_address_1.single = '3000::5'
next_hop_address_1.update()

print('\n  step 3. create two devices under the port2, protocol stack: eth/vlan/ipv6/bgpv6.\n')
# config device groups 'West Side - Device group 1' unde the port 'Ethernet - 002'
device_group_west_1 = config.create_device_groups('WestSideDevicegroup1')
device_group_west_1.ports = ['Ethernet2']
device_group_west_1.update()

# create 'Device 2' under the device_group_west 
devices_2 = device_group_west_1.create_devices('Device2')

# set the device count
devices_2.device_count_per_port = 1
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

# create protocol IPv4
protocol_ipv6_2 = devices_2.create_protocols('IPV62')
protocol_ipv6_2.protocol_type = 'IPV6'
protocol_ipv6_2.parent_link = 'Vlan3'
protocol_ipv6_2.update()

# # config mac addr
eth_2 = protocol_eth_2.ethernet()
eth_2.update()

eth_2_mac = eth_2.mac()
eth_2_mac.pattern_type = 'INCREMENT'
eth_2_mac.update()

eth_2_mac_incr = eth_2_mac.increment()
eth_2_mac_incr.start = '00:20:94:00:00:01'
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

# config ipv6 address
ipv6_2 = protocol_ipv6_2.ipv6()
ipv6_2.update()

ipv6_2_src_addr = ipv6_2.source_address()
ipv6_2_src_addr.pattern_type = 'SINGLE'
ipv6_2_src_addr.single = '2000::11'
ipv6_2_src_addr.update()

ipv6_2_gw_addr = ipv6_2.gateway_address()
ipv6_2_gw_addr.pattern_type = 'SINGLE'
ipv6_2_gw_addr.single = '2000::1'
ipv6_2_gw_addr.update()

#create and config BFDv4 protocol
protocol_bfdv6_2 = devices_2.create_protocols('BFDV62')
protocol_bfdv6_2.protocol_type = 'BFDV6'
protocol_bfdv6_2.parent_link = 'IPV62'
protocol_bfdv6_2.update()

bfdv6_2 = protocol_bfdv6_2.bfdv6()
bfdv6_2.update()

transmit_interval = bfdv6_2.transmit_interval()
transmit_interval.pattern_type = 'SINGLE'
transmit_interval.single = '20'
transmit_interval.update()

receive_interval = bfdv6_2.receive_interval()
receive_interval.pattern_type = 'SINGLE'
receive_interval.single = '30'
receive_interval.update()

echo_receive_interval = bfdv6_2.echo_receive_interval()
echo_receive_interval.pattern_type = 'SINGLE'
echo_receive_interval.single = '40'
echo_receive_interval.update()

#create and config BGPv4 protocol
protocol_bgp_2 = devices_2.create_protocols('BGPV62')
protocol_bgp_2.protocol_type = 'BGPV6'
protocol_bgp_2.parent_link = 'IPV62'
protocol_bgp_2.update()

bgpv6_2 = protocol_bgp_2.bgpv6()
bgpv6_2.update()

dut_ipv6_address_2 = bgpv6_2.dut_ipv6_address()
dut_ipv6_address_2.pattern_type = 'SINGLE'
dut_ipv6_address_2.single = '2000::1'
dut_ipv6_address_2.update()

hold_time_interval_2 = bgpv6_2.hold_time_interval()
hold_time_interval_2.pattern_type = 'SINGLE'
hold_time_interval_2.single = '100'
hold_time_interval_2.update()

keep_alive_interval_2 = bgpv6_2.keep_alive_interval()
keep_alive_interval_2.pattern_type = 'SINGLE'
keep_alive_interval_2.single = '50'
keep_alive_interval_2.update()

as_number_2_byte_2 = bgpv6_2.create_as_number_2_byte()
as_number_2 = as_number_2_byte_2.as_number()
as_number_2.pattern_type = 'SINGLE'
as_number_2.single = '10'
as_number_2.update()

dut_as_number_2 = as_number_2_byte_2.dut_as_number()
dut_as_number_2.pdattern_type = 'SINGLE'
dut_as_number_2.single = '20'
dut_as_number_2.update()

# create simulated_networks under the device_group_east
simulated_networks_2 = device_group_west_1.create_simulated_networks('SimulatedNetworks2')
simulated_networks_2.device_count_per_port = 1
simulated_networks_2.parent_link = 'Device2'
simulated_networks_2.update()

# create 'BGPV6 Route Range' under the simulated_networks_1
networks_2 = simulated_networks_2.create_networks('BGPV6Networks2')
networks_2.flow_link = 'BGPV62'
networks_2.network_type = 'BGPV6_ROUTE_RANGE'
networks_2.update()

#config the bgpv6_route_range_1
bgpv6_route_range_2 = networks_2.bgpv6_route_range()
bgpv6_route_range_2.update()

address_2 = bgpv6_route_range_2.address()
address_2.pattern_type = 'SINGLE'
address_2.single = '3000::11'
address_2.update()

prefix_length_2 = bgpv6_route_range_2.prefix_length()
prefix_length_2.pattern_type = 'SINGLE'
prefix_length_2.single = '24'
prefix_length_2.update()

as_path_2 = bgpv6_route_range_2.as_path()
as_path_2.pattern_type = 'SINGLE'
as_path_2.single = '20'
as_path_2.update()

next_hop_address_2= bgpv6_route_range_2.next_hop_address()
next_hop_address_2.pattern_type = 'SINGLE'
next_hop_address_2.single = '3000::13'
next_hop_address_2.update()

#  start BFDV6 protocol
print('\n  start BFDV4 protocol\n')
bfdv6_control_input1 = config.Bfdv6ControlInput()
bfdv6_control_input1.targets.append('BFDV61')
bfdv6_control_input1.targets.append('BFDV62')
bfdv6_control_input1.mode = 'START'
config.bfdv6_control(bfdv6_control_input1)

#start BGP protocol
print('\n  step 4. start BGP protocol\n')
bgpv6_control_input1 = config.Bgpv6ControlInput()
bgpv6_control_input1.targets.append('BGPV61')
bgpv6_control_input1.targets.append('BGPV62')
bgpv6_control_input1.mode = 'START'
config.bgpv6_control(bgpv6_control_input1)

time.sleep(30)

#  step 5. Get the BGP statistics
print('\n  step 5. Get the BGP statistics\n')
statistics = session.statistics()
print('%s \n' % statistics._values)
bgpv6_statistics_1 = statistics.bgpv6_statistics('Device1')
bgpv6_statistics_2 = statistics.bgpv6_statistics('Device2')
print(bgpv6_statistics_1._values)
print(bgpv6_statistics_2._values)

bgp1_state = bgpv6_statistics_1._values['router-state']
bgp2_state = bgpv6_statistics_2._values['router-state']

if (bgp1_state == 'ESTABLISHED'and bgp2_state == 'ESTABLISHED') :
    print('*' * 40)
    print ("\n Info :BGP session established successful \n")
    print('*' * 40)
else :
    print ("\n <error> Failed to establish bgp sessions")
    sys.exit();

print('\n  Get the BFDv6 statistics\n')
bfdv6_statistics_1 = statistics.bfdv6_statistics('Device1')
bfdv6_statistics_2 = statistics.bfdv6_statistics('Device2')
print(bfdv6_statistics_1._values)
print(bfdv6_statistics_2._values)

# create BOUND streamblock - IPv4 endpoints
device_traffic = config.create_device_traffic('IPV6Stream1')

# ENPOINTS: Devices
device_traffic.encapsulation = "IPV6"
device_traffic.sources = ['SimulatedNetworks1']
device_traffic.destinations = ['SimulatedNetworks2']
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

#  stop the BGP protocol
print('\n stop the BGP protocol\n')
bgpv6_control_input1 = config.Bgpv6ControlInput()
bgpv6_control_input1.targets.append('BGPV61')
bgpv6_control_input1.targets.append('BGPV62')
bgpv6_control_input1.mode = 'STOP'
config.bgpv6_control(bgpv6_control_input1)

#  stop BFDV6 protocol
print('\n  stop BFDV6 protocol\n')
bfdv6_control_input1 = config.Bfdv6ControlInput()
bfdv6_control_input1.mode = 'STOP'
config.bfdv6_control(bfdv6_control_input1)

#disconnect ports
port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)
session.delete()
