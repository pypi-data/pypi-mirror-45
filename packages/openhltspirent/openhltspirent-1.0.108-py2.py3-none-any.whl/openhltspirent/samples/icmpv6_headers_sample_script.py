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

print('\n  step 2. create ipv6 raw streamblock\n')
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
eth_src_addr_1_incr.count = '2'
eth_src_addr_1_incr.update()

eth_dest_addr = ethernet_frame_1.destination()
eth_dest_addr.pattern_type = 'SINGLE'
eth_dest_addr.single = '00:10:94:00:00:80'
eth_dest_addr.update()

#ipv6
frame_6 = port_traffic_1.create_frames('Ipv61')
frame_6.frame_type = 'IPV6'
frame_6.update()

ipv6_frame_1 = frame_6.ipv6()
ipv6_frame_1.update()
 
ipv6_source_addr = ipv6_frame_1.source_address()
ipv6_source_addr.pattern_type = 'SINGLE'
ipv6_source_addr.single = '2000::1'
ipv6_source_addr.update()

ipv6_dest_addr = ipv6_frame_1.destination_address()
ipv6_dest_addr.pattern_type = 'SINGLE'
ipv6_dest_addr.single = '3000::1'
ipv6_dest_addr.update()

#ICMPV6 ECHO REPLY
frame_3 = port_traffic_1.create_frames('icmpv6_echoreply')
frame_3.frame_type = 'ICMPV6_ECHO_REPLY'
frame_3.update()

echo_icmpv6reply_frame_1 = frame_3.icmpv6_echo_reply()
echo_icmpv6reply_frame_1.update()

code_1 = echo_icmpv6reply_frame_1.code()
code_1.pattern_type = 'SINGLE'
code_1.single = '100'
code_1.update()

checksum_1 = echo_icmpv6reply_frame_1.checksum()
checksum_1.pattern_type = 'SINGLE'
checksum_1.single = '1000'
checksum_1.update()

sequence_number_1 = echo_icmpv6reply_frame_1.sequence_number()
sequence_number_1.pattern_type = 'INCREMENT'
sequence_number_1.update()

sequence_number_1_incr = sequence_number_1.increment()
sequence_number_1_incr.start = '1'
sequence_number_1_incr.step = '2'
sequence_number_1_incr.count = '2'
sequence_number_1_incr.update()

echo_data_1 = echo_icmpv6reply_frame_1.echo_data()
echo_data_1.pattern_type = 'DECREMENT'
echo_data_1.update()

echo_data_1_incr = echo_data_1.decrement()
echo_data_1_incr.start = '1000'
echo_data_1_incr.step = '0001'
echo_data_1_incr.count = '5'
echo_data_1_incr.update()

identifier_1 = echo_icmpv6reply_frame_1.identifier()
identifier_1.pattern_type = 'SINGLE'
identifier_1.single = '3000'
identifier_1.update()

print('\n  step 3. create ipv6 raw streamblock\n')
port_traffic_2 = config.create_port_traffic('Stream2')
port_traffic_2.source = 'Ethernet1'
port_traffic_2.update()

#Config Frame Size
frame_length_1 = port_traffic_2.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '512'
frame_length_1.update()


frame_1 = port_traffic_2.create_frames('Ethernet2')
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
eth_src_addr_1_incr.count = '2'
eth_src_addr_1_incr.update()

eth_dest_addr = ethernet_frame_1.destination()
eth_dest_addr.pattern_type = 'SINGLE'
eth_dest_addr.single = '00:10:94:00:00:80'
eth_dest_addr.update()

## ipv6
frame_6 = port_traffic_2.create_frames('Ipv62')
frame_6.frame_type = 'IPV6'
frame_6.update()

ipv6_frame_1 = frame_6.ipv6()
ipv6_frame_1.update()
 
ipv6_source_addr = ipv6_frame_1.source_address()
ipv6_source_addr.pattern_type = 'SINGLE'
ipv6_source_addr.single = '2000::1'
ipv6_source_addr.update()

ipv6_dest_addr = ipv6_frame_1.destination_address()
ipv6_dest_addr.pattern_type = 'SINGLE'
ipv6_dest_addr.single = '3000::1'
ipv6_dest_addr.update()

#ICMPV6_DESTINATION_UNREACHABLE
frame_3 = port_traffic_2.create_frames('icmpv6_destination_unreachable')
frame_3.frame_type = 'ICMPV6_DESTINATION_UNREACHABLE'
frame_3.update()

echo_icmpv6_dest_unreach_1 = frame_3.icmpv6_destination_unreachable()
echo_icmpv6_dest_unreach_1.update()

code_1 = echo_icmpv6_dest_unreach_1.code()
code_1.pattern_type = 'SINGLE'
code_1.single = '3'
code_1.update()

checksum_1 = echo_icmpv6_dest_unreach_1.checksum()
checksum_1.pattern_type = 'SINGLE'
checksum_1.single = '1000'
checksum_1.update()

ipv6_source_address_1 = echo_icmpv6_dest_unreach_1.ipv6_source_address()
ipv6_source_address_1.pattern_type = 'INCREMENT'
ipv6_source_address_1.update()

ipv6_source_address_1_incr = ipv6_source_address_1.increment()
ipv6_source_address_1_incr.start = '3000::21'
ipv6_source_address_1_incr.step = '0000::1'
ipv6_source_address_1_incr.count = '4'
ipv6_source_address_1_incr.update()

destination_address_1 = echo_icmpv6_dest_unreach_1.ipv6_destination_address()
destination_address_1.pattern_type = 'SINGLE'
destination_address_1.single = '4000::1'
destination_address_1.update()

ipv6_gateway_address_1 = echo_icmpv6_dest_unreach_1.ipv6_gateway_address()
ipv6_gateway_address_1.pattern_type = 'SINGLE'
ipv6_gateway_address_1.single = '3000::1'
ipv6_gateway_address_1.update()

ipv6_hop_limit_1 = echo_icmpv6_dest_unreach_1.ipv6_hop_limit()
ipv6_hop_limit_1.pattern_type = 'DECREMENT'
ipv6_hop_limit_1.update()

ipv6_hop_limit_1_incr = ipv6_hop_limit_1.decrement()
ipv6_hop_limit_1_incr.start = '100'
ipv6_hop_limit_1_incr.step = '2'
ipv6_hop_limit_1_incr.count = '2'
ipv6_hop_limit_1_incr.update()

traffic_class_1 = echo_icmpv6_dest_unreach_1.ipv6_traffic_class()
traffic_class_1.pattern_type = 'SINGLE'
traffic_class_1.single = '10'
traffic_class_1.update()

ipv6_next_header_1 = echo_icmpv6_dest_unreach_1.ipv6_next_header()
ipv6_next_header_1.pattern_type = 'SINGLE'
ipv6_next_header_1.single = '59'
ipv6_next_header_1.update()

ipv6_flow_label_1 = echo_icmpv6_dest_unreach_1.ipv6_flow_label()
ipv6_flow_label_1.pattern_type = 'SINGLE'
ipv6_flow_label_1.single = '1000'
ipv6_flow_label_1.update()

print('\n  step 4. create ipv6 raw streamblock\n')
port_traffic_3 = config.create_port_traffic('Stream3')
port_traffic_3.source = 'Ethernet2'
port_traffic_3.update()

#Config Frame Size
frame_length_1 = port_traffic_3.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '512'
frame_length_1.update()


frame_1 = port_traffic_3.create_frames('Ethernet3')
frame_1.frame_type = 'ETHERNET'
frame_1.update()

# ethernet header
ethernet_frame_3 = frame_1.ethernet()
ethernet_frame_3.update()

eth_src_addr_1 = ethernet_frame_3.source()
eth_src_addr_1.pattern_type = 'INCREMENT'
eth_src_addr_1.update()

eth_src_addr_1_incr = eth_src_addr_1.increment()
eth_src_addr_1_incr.start = '00:10:94:00:00:12'
eth_src_addr_1_incr.step = '00:00:00:00:00:02'
eth_src_addr_1_incr.count = '2'
eth_src_addr_1_incr.update()

eth_dest_addr = ethernet_frame_1.destination()
eth_dest_addr.pattern_type = 'SINGLE'
eth_dest_addr.single = '00:10:94:00:00:80'
eth_dest_addr.update()

#ipv6
frame_6 = port_traffic_3.create_frames('Ipv63')
frame_6.frame_type = 'IPV6'
frame_6.update()

ipv6_frame_1 = frame_6.ipv6()
ipv6_frame_1.update()
 
ipv6_source_addr = ipv6_frame_1.source_address()
ipv6_source_addr.pattern_type = 'SINGLE'
ipv6_source_addr.single = '2000::1'
ipv6_source_addr.update()

ipv6_dest_addr = ipv6_frame_1.destination_address()
ipv6_dest_addr.pattern_type = 'SINGLE'
ipv6_dest_addr.single = '3000::1'
ipv6_dest_addr.update()

#ICMPV6_TIME_EXCEEDED
frame_3 = port_traffic_3.create_frames('icmpv6_time_exceeded')
frame_3.frame_type = 'ICMPV6_TIME_EXCEEDED'
frame_3.update()

icmpv6_time_exceeded_1 = frame_3.icmpv6_time_exceeded()
icmpv6_time_exceeded_1.update()

code_1 = icmpv6_time_exceeded_1.code()
code_1.pattern_type = 'SINGLE'
code_1.single = '100'
code_1.update()

checksum_1 = icmpv6_time_exceeded_1.checksum()
checksum_1.pattern_type = 'SINGLE'
checksum_1.single = '1000'
checksum_1.update()

ipv6_source_address_1 = icmpv6_time_exceeded_1.ipv6_source_address()
ipv6_source_address_1.pattern_type = 'INCREMENT'
ipv6_source_address_1.update()

ipv6_source_address_1_incr = ipv6_source_address_1.increment()
ipv6_source_address_1_incr.start = '3000::21'
ipv6_source_address_1_incr.step = '0000::1'
ipv6_source_address_1_incr.count = '5'
ipv6_source_address_1_incr.update()

destination_address_1 = icmpv6_time_exceeded_1.ipv6_destination_address()
destination_address_1.pattern_type = 'SINGLE'
destination_address_1.single = '4000::1'
destination_address_1.update()

ipv6_gateway_address_1 = icmpv6_time_exceeded_1.ipv6_gateway_address()
ipv6_gateway_address_1.pattern_type = 'SINGLE'
ipv6_gateway_address_1.single = '3000::1'
ipv6_gateway_address_1.update()

ipv6_hop_limit_1 = icmpv6_time_exceeded_1.ipv6_hop_limit()
ipv6_hop_limit_1.pattern_type = 'DECREMENT'
ipv6_hop_limit_1.update()

ipv6_hop_limit_1_incr = ipv6_hop_limit_1.decrement()
ipv6_hop_limit_1_incr.start = '100'
ipv6_hop_limit_1_incr.step = '2'
ipv6_hop_limit_1_incr.count = '5'
ipv6_hop_limit_1_incr.update()

traffic_class_1 = icmpv6_time_exceeded_1.ipv6_traffic_class()
traffic_class_1.pattern_type = 'SINGLE'
traffic_class_1.single = '10'
traffic_class_1.update()

ipv6_next_header_1 = icmpv6_time_exceeded_1.ipv6_next_header()
ipv6_next_header_1.pattern_type = 'SINGLE'
ipv6_next_header_1.single = '59'
ipv6_next_header_1.update()

ipv6_flow_label_1 = icmpv6_time_exceeded_1.ipv6_flow_label()
ipv6_flow_label_1.pattern_type = 'SINGLE'
ipv6_flow_label_1.single = '1000'
ipv6_flow_label_1.update()

print('\n  step 4. start traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.targets.append('Stream2')
traffic_control_input1.targets.append('Stream3')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

time.sleep(5)

print('\n  step 6. stop traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.targets.append('Stream2')
traffic_control_input1.targets.append('Stream3')
traffic_control_input1.mode = 'STOP'
config.traffic_control(traffic_control_input1)

print('\n  step 7. get statistics\n')
statistics = session.statistics()

statistics_traffic = statistics.port_traffic('Stream1')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

statistics_traffic = statistics.port_traffic('Stream2')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

statistics_traffic = statistics.port_traffic('Stream3')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

statistics_traffic = statistics.port('Ethernet1')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

statistics_traffic = statistics.port('Ethernet2')
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
