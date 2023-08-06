###Test Steps
    #Step 1:  Create a session and connect to two back to back stc ports
    #Step 2:  Configue 2 bgp devices with bfd on each port
    #Step 3:  Configure 2 bgp a routes one each bgp device
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

print('\n  step 2. create devices under the port1, protocol stack: eth/vlan/vlan/ipv4/bgpv4.\n')
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

#create and config BFDv4 protocol
protocol_bfdv4_1 = devices_1.create_protocols('BFDV41')
protocol_bfdv4_1.protocol_type = 'BFDV4'
protocol_bfdv4_1.parent_link = 'IPV41'
protocol_bfdv4_1.update()

bfdv4_1 = protocol_bfdv4_1.bfdv4()
bfdv4_1.update()

transmit_interval = bfdv4_1.transmit_interval()
transmit_interval.pattern_type = 'SINGLE'
transmit_interval.single = '20'
transmit_interval.update()

receive_interval = bfdv4_1.receive_interval()
receive_interval.pattern_type = 'SINGLE'
receive_interval.single = '30'
receive_interval.update()

echo_receive_interval = bfdv4_1.echo_receive_interval()
echo_receive_interval.pattern_type = 'SINGLE'
echo_receive_interval.single = '40'
echo_receive_interval.update()

#create and config BGPv4 protocol
protocol_bgp_1 = devices_1.create_protocols('BGPV41')
protocol_bgp_1.protocol_type = 'BGPV4'
protocol_bgp_1.parent_link = 'IPV41'
protocol_bgp_1.update()

bgpv4_1 = protocol_bgp_1.bgpv4()
bgpv4_1.update()

dut_ipv4_address_1 = bgpv4_1.dut_ipv4_address()
dut_ipv4_address_1.pattern_type = 'SINGLE'
dut_ipv4_address_1.single = '192.85.1.13'
dut_ipv4_address_1.update()

hold_time_interval_1 = bgpv4_1.hold_time_interval()
hold_time_interval_1.pattern_type = 'SINGLE'
hold_time_interval_1.single = '100'
hold_time_interval_1.update()

keep_alive_interval_1 = bgpv4_1.keep_alive_interval()
keep_alive_interval_1.pattern_type = 'SINGLE'
keep_alive_interval_1.single = '50'
keep_alive_interval_1.update()

as_number_2_byte_1 = bgpv4_1.create_as_number_2_byte()
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

# create 'BGPV4 Route Range' under the simulated_networks_1
networks_1 = simulated_networks_1.create_networks('BGPV4Networks1')
networks_1.flow_link = 'BGPV41'
networks_1.network_type = 'BGPV4_ROUTE_RANGE'
networks_1.update()

#config the bgpv4_route_range_1
bgpv4_route_range_1 = networks_1.bgpv4_route_range()
bgpv4_route_range_1.update()

address_1 = bgpv4_route_range_1.address()
address_1.pattern_type = 'SINGLE'
address_1.single = '192.0.1.0'
address_1.update()

prefix_length_1 = bgpv4_route_range_1.prefix_length()
prefix_length_1.pattern_type = 'SINGLE'
prefix_length_1.single = '24'
prefix_length_1.update()

as_path_1 = bgpv4_route_range_1.as_path()
as_path_1.pattern_type = 'SINGLE'
as_path_1.single = '20'
as_path_1.update()

next_hop_address_1 = bgpv4_route_range_1.next_hop_address()
next_hop_address_1.pattern_type = 'SINGLE'
next_hop_address_1.single = '192.85.1.3'
next_hop_address_1.update()


print('\n  step 3. create two devices under the port2, protocol stack: eth/vlan/vlan/ipv4/bgpv4.\n')
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

#create and config BFDv4 protocol
protocol_bfdv4_2 = devices_2.create_protocols('BFDV42')
protocol_bfdv4_2.protocol_type = 'BFDV4'
protocol_bfdv4_2.parent_link = 'IPV42'
protocol_bfdv4_2.update()

bfdv4_2 = protocol_bfdv4_2.bfdv4()
bfdv4_2.update()

transmit_interval = bfdv4_2.transmit_interval()
transmit_interval.pattern_type = 'SINGLE'
transmit_interval.single = '20'
transmit_interval.update()

receive_interval = bfdv4_2.receive_interval()
receive_interval.pattern_type = 'SINGLE'
receive_interval.single = '30'
receive_interval.update()

echo_receive_interval = bfdv4_2.echo_receive_interval()
echo_receive_interval.pattern_type = 'SINGLE'
echo_receive_interval.single = '40'
echo_receive_interval.update()

#create and config BGPv4 protocol
protocol_bgp_2 = devices_2.create_protocols('BGPV42')
protocol_bgp_2.protocol_type = 'BGPV4'
protocol_bgp_2.parent_link = 'IPV42'
protocol_bgp_2.update()

bgpv4_2 = protocol_bgp_2.bgpv4()
bgpv4_2.update()

dut_ipv4_address_2 = bgpv4_2.dut_ipv4_address()
dut_ipv4_address_2.pattern_type = 'SINGLE'
dut_ipv4_address_2.single = '192.85.1.3'
dut_ipv4_address_2.update()

hold_time_interval_2 = bgpv4_2.hold_time_interval()
hold_time_interval_2.pattern_type = 'SINGLE'
hold_time_interval_2.single = '100'
hold_time_interval_2.update()

keep_alive_interval_2 = bgpv4_2.keep_alive_interval()
keep_alive_interval_2.pattern_type = 'SINGLE'
keep_alive_interval_2.single = '50'
keep_alive_interval_2.update()

as_number_2_byte_2 = bgpv4_2.create_as_number_2_byte()
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

# create 'BGPV4 Route Range' under the simulated_networks_1
networks_2 = simulated_networks_2.create_networks('BGPV4Networks2')
networks_2.flow_link = 'BGPV42'
networks_2.network_type = 'BGPV4_ROUTE_RANGE'
networks_2.update()

#config the bgpv4_route_range_1
bgpv4_route_range_2 = networks_2.bgpv4_route_range()
bgpv4_route_range_2.update()

address_2 = bgpv4_route_range_2.address()
address_2.pattern_type = 'SINGLE'
address_2.single = '192.0.1.0'
address_2.update()

prefix_length_2 = bgpv4_route_range_2.prefix_length()
prefix_length_2.pattern_type = 'SINGLE'
prefix_length_2.single = '24'
prefix_length_2.update()

as_path_2 = bgpv4_route_range_2.as_path()
as_path_2.pattern_type = 'SINGLE'
as_path_2.single = '20'
as_path_2.update()

next_hop_address_2= bgpv4_route_range_2.next_hop_address()
next_hop_address_2.pattern_type = 'SINGLE'
next_hop_address_2.single = '192.85.1.13'
next_hop_address_2.update()

#  start BFD protocol
print('\n  start BFDV4 protocol\n')
bfdv4_control_input1 = config.Bfdv4ControlInput()
bfdv4_control_input1.targets.append('BFDV41')
bfdv4_control_input1.targets.append('BFDV42')
bfdv4_control_input1.mode = 'START'
config.bfdv4_control(bfdv4_control_input1)

#  start BGP protocol
print('\n  step 4. start BGP protocol\n')
bgpv4_control_input1 = config.Bgpv4ControlInput()
bgpv4_control_input1.targets.append('BGPV41')
bgpv4_control_input1.targets.append('BGPV42')
bgpv4_control_input1.mode = 'START'
config.bgpv4_control(bgpv4_control_input1)

time.sleep(30)

#  step 5. Get the BGP statistics
print('\n Get the BGP statistics\n')
statistics = session.statistics()
print('%s \n' % statistics._values)
bgpv4_statistics_1 = statistics.bgpv4_statistics('Device1')
bgpv4_statistics_2 = statistics.bgpv4_statistics('Device2')
print(bgpv4_statistics_1._values)
print(bgpv4_statistics_2._values)

bgp1_state = bgpv4_statistics_1._values['router-state']
bgp2_state = bgpv4_statistics_2._values['router-state']

if (bgp1_state == 'ESTABLISHED'and bgp2_state == 'ESTABLISHED') :
    print('*' * 40)
    print ("\n Info :BGP session established successful \n")
    print('*' * 40)
else :
    print ("\nFailed to establish bgp sessions")
    sys.exit();

print('\n  Get the BFDv4 statistics\n')
bfdv4_statistics_1 = statistics.bfdv4_statistics('Device1')
bfdv4_statistics_2 = statistics.bfdv4_statistics('Device2')
print(bfdv4_statistics_1._values)
print(bfdv4_statistics_2._values)    
    
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
print('\n Get traffic statistics\n')
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
    print ("\nTraffic is not transmitted successfully")
    sys.exit();

#  stop BFD protocol
print('\n  stop BFDV4 protocol\n')
bfdv4_control_input1 = config.Bfdv4ControlInput()
bfdv4_control_input1.mode = 'STOP'
config.bfdv4_control(bfdv4_control_input1)

#  stop BGP protocol
print('\n  step 4. stop BGP protocol\n')
bgpv4_control_input1 = config.Bgpv4ControlInput()
bgpv4_control_input1.mode = 'STOP'
config.bgpv4_control(bgpv4_control_input1)


#  start device-groups
print('\n  Start Devices \n')
device_groups_control_input1 = config.DeviceGroupsControlInput()
device_groups_control_input1.mode = 'START'
config.device_groups_control(device_groups_control_input1)

time.sleep(30)

#  step 5. Get the BGP statistics
print('\n Get the BGP statistics\n')
statistics = session.statistics()
print('%s \n' % statistics._values)
bgpv4_statistics_1 = statistics.bgpv4_statistics('Device1')
bgpv4_statistics_2 = statistics.bgpv4_statistics('Device2')
print(bgpv4_statistics_1._values)
print(bgpv4_statistics_2._values)

bgp1_state = bgpv4_statistics_1._values['router-state']
bgp2_state = bgpv4_statistics_2._values['router-state']

if (bgp1_state == 'ESTABLISHED'and bgp2_state == 'ESTABLISHED') :
    print('*' * 40)
    print ("\n Info :BGP session established successful \n")
    print('*' * 40)
else :
    print ("\nFailed to establish bgp sessions")
    #sys.exit();

print('\n  Get the BFDv4 statistics\n')
bfdv4_statistics_1 = statistics.bfdv4_statistics('Device1')
bfdv4_statistics_2 = statistics.bfdv4_statistics('Device2')
print(bfdv4_statistics_1._values)
print(bfdv4_statistics_2._values)


#  stop device-groups
print('\n  Stop Devices \n')
device_groups_control_input1 = config.DeviceGroupsControlInput()
device_groups_control_input1.targets.append('EastSideDevicegroup1')
device_groups_control_input1.targets.append('WestSideDevicegroup1')
device_groups_control_input1.mode = 'STOP'
config.device_groups_control(device_groups_control_input1)


#disconnect ports
port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

session.delete()
