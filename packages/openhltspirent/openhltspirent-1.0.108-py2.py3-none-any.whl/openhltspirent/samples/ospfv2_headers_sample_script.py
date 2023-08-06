# test stpes:
#  1. create and connect two ports

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
print("protnumber",portnumber)

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

print('\n  step 2. create ipv4 raw streamblock\n')
port_traffic_1 = config.create_port_traffic('Stream1')
port_traffic_1.source = 'Ethernet1'
port_traffic_1.update()

#Config Frame Size
frame_length_1 = port_traffic_1.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '512'
frame_length_1.update()


frame_1 = port_traffic_1.create_frames('Ethernet1')
frame_1.frame_type = 'ETHERNET'
frame_1.update()

# ethernet header
ethernet_frame_1 = frame_1.ethernet()
ethernet_frame_1.update()

eth_src_addr_1 = ethernet_frame_1.source()
eth_src_addr_1.pattern_type = 'INCREMENT'
eth_src_addr_1.update()

eth_src_addr_1_incr = eth_src_addr_1.increment()
eth_src_addr_1_incr.start = '00:10:94:00:00:12'
eth_src_addr_1_incr.step = '00:00:00:00:00:02'
eth_src_addr_1_incr.count = '10'
eth_src_addr_1_incr.update()

eth_dest_addr = ethernet_frame_1.destination()
eth_dest_addr.pattern_type = 'SINGLE'
eth_dest_addr.single = '00:10:94:00:00:80'
eth_dest_addr.update()

#ipv4
frame_4 = port_traffic_1.create_frames('Ipv41')
frame_4.frame_type = 'IPV4'
frame_4.update()

ipv4_frame_1 = frame_4.ipv4()
ipv4_frame_1.update()

ipv4_source_addr = ipv4_frame_1.source_address()
ipv4_source_addr.pattern_type = 'SINGLE'
ipv4_source_addr.single = '10.10.10.10'
ipv4_source_addr.update()

ipv4_dest_addr = ipv4_frame_1.destination_address()
ipv4_dest_addr.pattern_type = 'SINGLE'
ipv4_dest_addr.single = '20.20.20.20'
ipv4_dest_addr.update()

ipv4_ttl = ipv4_frame_1.ttl()
ipv4_ttl.pattern_type = 'SINGLE'
ipv4_ttl.single = '243'
ipv4_ttl.update()

#OSPFv2 Hello
frame_1 = port_traffic_1.create_frames('ospf_hello1')
frame_1.frame_type = 'OSPFV2_HELLO'
frame_1.update()

hello_frame_1 = frame_1.ospfv2_hello()
hello_frame_1.update()

designated_router = hello_frame_1.designated_router_address()
designated_router.pattern_type = 'SINGLE'
designated_router.single = '11.1.1.1'
designated_router.update()

backup_designated_router = hello_frame_1.backup_designated_router_address()
backup_designated_router.pattern_type = 'SINGLE'
backup_designated_router.single = '12.1.1.1'
backup_designated_router.update()

area_id = hello_frame_1.area_id()
area_id.pattern_type = 'INCREMENT'
area_id.update()

area_id_incr = area_id.increment()
area_id_incr.start = '10.1.1.1'
area_id_incr.step = '0.0.0.2'
area_id_incr.count = '10'
area_id_incr.update()

router_id = hello_frame_1.router_id()
router_id.pattern_type = 'SINGLE'
router_id.single = '13.1.1.1'
router_id.update()

reserved_bit_7 = hello_frame_1.options_reserved_bit_7()
reserved_bit_7.pattern_type = 'SINGLE'
reserved_bit_7.single = '1'
reserved_bit_7.update()

reserved_bit_6 = hello_frame_1.options_reserved_bit_6()
reserved_bit_6.pattern_type = 'SINGLE'
reserved_bit_6.single = '1'
reserved_bit_6.update()

options_dc_bit = hello_frame_1.options_dc_bit()
options_dc_bit.pattern_type = 'SINGLE'
options_dc_bit.single = '1'
options_dc_bit.update()

options_dc_bit = hello_frame_1.options_mc_bit()
options_dc_bit.pattern_type = 'SINGLE'
options_dc_bit.single = '1'
options_dc_bit.update()

auth_type = hello_frame_1.auth_type()
auth_type.pattern_type = 'SINGLE'
auth_type.single = 'MD5'
auth_type.update()

auth_value1 = hello_frame_1.auth_value1()
auth_value1.pattern_type = 'SINGLE'
auth_value1.single = '254'
auth_value1.update()

auth_value2 = hello_frame_1.auth_value2()
auth_value2.pattern_type = 'SINGLE'
auth_value2.single = '10000000'
auth_value2.update()

neighbors = hello_frame_1.create_neighbors('neighbors_1')
neighbors.update()

neighbors_id = neighbors.neighbors_id()
neighbors_id.pattern_type = 'SINGLE'
neighbors_id.single = '1.1.1.1'
neighbors_id.update()

print('\n  step 4. strat traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

time.sleep(5)

print('\n  step 6. stop traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.mode = 'STOP'
config.traffic_control(traffic_control_input1)

print('\n  step 7. get statistics\n')
statistics = session.statistics()

statistics_traffic = statistics.port_traffic('Stream1')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

statistics_traffic = statistics.port('Ethernet1')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

#disconnect ports
port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

print('\n  step 9. delete session\n')
session.delete()
