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
eth_src_addr_1_incr.count = '2'
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

#ICMP Echo Request
frame_7 = port_traffic_1.create_frames('icmp_echorequest')
frame_7.frame_type = 'ICMP_ECHO_REQUEST'
frame_7.update()

echo_request_frame_1 = frame_7.icmp_echo_request()
echo_request_frame_1.update()

code_1 = echo_request_frame_1.code()
code_1.pattern_type = 'SINGLE'
code_1.single = '100'
code_1.update()

checksum_1 = echo_request_frame_1.checksum()
checksum_1.pattern_type = 'SINGLE'
checksum_1.single = '1000'
checksum_1.update()

sequence_number_1 = echo_request_frame_1.sequence_number()
sequence_number_1.pattern_type = 'INCREMENT'
sequence_number_1.update()

sequence_number_1_incr = sequence_number_1.increment()
sequence_number_1_incr.start = '1'
sequence_number_1_incr.step = '2'
sequence_number_1_incr.count = '2'
sequence_number_1_incr.update()

echo_data_1 = echo_request_frame_1.echo_data()
echo_data_1.pattern_type = 'INCREMENT'
echo_data_1.update()

echo_data_1_incr = echo_data_1.increment()
echo_data_1_incr.start = '1000'
echo_data_1_incr.step = '0001'
echo_data_1_incr.count = '2'
echo_data_1_incr.update()

identifier_1 = echo_request_frame_1.identifier()
identifier_1.pattern_type = 'SINGLE'
identifier_1.single = '1000'
identifier_1.update()

print('\n  step 3. create ipv4 raw streamblock\n')
port_traffic_3 = config.create_port_traffic('Stream3')
port_traffic_3.source = 'Ethernet1'
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

#ipv4
frame_4 = port_traffic_3.create_frames('Ipv43')
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

#ICMP ECHO REPLY
frame_7 = port_traffic_3.create_frames('icmp_echoreply')
frame_7.frame_type = 'ICMP_ECHO_REPLY'
frame_7.update()

echo_reply_frame_1 = frame_7.icmp_echo_reply()
echo_reply_frame_1.update()

code_1 = echo_reply_frame_1.code()
code_1.pattern_type = 'SINGLE'
code_1.single = '100'
code_1.update()

checksum_1 = echo_reply_frame_1.checksum()
checksum_1.pattern_type = 'SINGLE'
checksum_1.single = '1000'
checksum_1.update()

sequence_number_1 = echo_reply_frame_1.sequence_number()
sequence_number_1.pattern_type = 'INCREMENT'
sequence_number_1.update()

sequence_number_1_incr = sequence_number_1.increment()
sequence_number_1_incr.start = '1'
sequence_number_1_incr.step = '2'
sequence_number_1_incr.count = '10'
sequence_number_1_incr.update()

echo_data_1 = echo_reply_frame_1.echo_data()
echo_data_1.pattern_type = 'DECREMENT'
echo_data_1.update()

echo_data_1_incr = echo_data_1.increment()
echo_data_1_incr.start = '1000'
echo_data_1_incr.step = '0001'
echo_data_1_incr.count = '5'
echo_data_1_incr.update()

identifier_1 = echo_request_frame_1.identifier()
identifier_1.pattern_type = 'SINGLE'
identifier_1.single = '1000'
identifier_1.update()

print('\n  step 4. create ipv4 raw streamblock\n')
port_traffic_2 = config.create_port_traffic('Stream2')
port_traffic_2.source = 'Ethernet2'
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

#ipv4
frame_4 = port_traffic_2.create_frames('Ipv42')
frame_4.frame_type = 'IPV4'
frame_4.update()

ipv4_frame_1 = frame_4.ipv4()
ipv4_frame_1.update()

ipv4_source_addr = ipv4_frame_1.source_address()
ipv4_source_addr.pattern_type = 'SINGLE'
ipv4_source_addr.single = '11.11.11.11'
ipv4_source_addr.update()

ipv4_dest_addr = ipv4_frame_1.destination_address()
ipv4_dest_addr.pattern_type = 'SINGLE'
ipv4_dest_addr.single = '22.22.22.22'
ipv4_dest_addr.update()

ipv4_ttl = ipv4_frame_1.ttl()
ipv4_ttl.pattern_type = 'SINGLE'
ipv4_ttl.single = '243'
ipv4_ttl.update()

#ICMP_TIME_EXCEEDED
frame_3 = port_traffic_2.create_frames('icmp_time_exceeded')
frame_3.frame_type = 'ICMP_TIME_EXCEEDED'
frame_3.update()

icmp_time_exceeded_frame_1 = frame_3.icmp_time_exceeded()
icmp_time_exceeded_frame_1.update()

code = icmp_time_exceeded_frame_1.code()
code.pattern_type = 'SINGLE'
code.single = '100'
code.update()

ipv4_source_address_3 = icmp_time_exceeded_frame_1.ipv4_source_address()
ipv4_source_address_3.pattern_type = 'SINGLE'
ipv4_source_address_3.single = '10.10.10.10'
ipv4_source_address_3.update()

ipv4_destination_address = icmp_time_exceeded_frame_1.ipv4_destination_address()
ipv4_destination_address.pattern_type = 'INCREMENT'
ipv4_destination_address.update()

ipv4_destination_address_3_incr = ipv4_destination_address.increment()
ipv4_destination_address_3_incr.start = '20.20.20.20'
ipv4_destination_address_3_incr.step = '0.0.0.4'
ipv4_destination_address_3_incr.count = '2'
ipv4_destination_address_3_incr.update()

reserved_bit = icmp_time_exceeded_frame_1.ipv4_reserved_bit()
reserved_bit.pattern_type = 'SINGLE'
reserved_bit.single = '1'
reserved_bit.update()

ipv4_checksum = icmp_time_exceeded_frame_1.ipv4_checksum()
ipv4_checksum.pattern_type = 'SINGLE'
ipv4_checksum.single = '100'
ipv4_checksum.update()

unused = icmp_time_exceeded_frame_1.unused()
unused.pattern_type = 'SINGLE'
unused.single = '2000'
unused.update()

print('\n  step 5. create ipv4 raw streamblock\n')
port_traffic_4 = config.create_port_traffic('Stream4')
port_traffic_4.source = 'Ethernet2'
port_traffic_4.update()

#Config Frame Size
frame_length_1 = port_traffic_4.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '512'
frame_length_1.update()

frame_1 = port_traffic_4.create_frames('Ethernet4')
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
frame_4 = port_traffic_4.create_frames('Ipv44')
frame_4.frame_type = 'IPV4'
frame_4.update()

ipv4_frame_1 = frame_4.ipv4()
ipv4_frame_1.update()

ipv4_source_addr = ipv4_frame_1.source_address()
ipv4_source_addr.pattern_type = 'SINGLE'
ipv4_source_addr.single = '11.11.11.11'
ipv4_source_addr.update()

ipv4_dest_addr = ipv4_frame_1.destination_address()
ipv4_dest_addr.pattern_type = 'SINGLE'
ipv4_dest_addr.single = '22.22.22.22'
ipv4_dest_addr.update()

ipv4_ttl = ipv4_frame_1.ttl()
ipv4_ttl.pattern_type = 'SINGLE'
ipv4_ttl.single = '243'
ipv4_ttl.update()

#ICMP redirect
frame_1 = port_traffic_1.create_frames('icmp_redirect')
frame_1.frame_type = 'ICMP_REDIRECT'
frame_1.update()

icmp_redirect_frame_1 = frame_1.icmp_redirect()
icmp_redirect_frame_1.update()

code = icmp_redirect_frame_1.code()
code.pattern_type = 'SINGLE'
code.single = '100'
code.update()

gateway_address = icmp_redirect_frame_1.gateway_address()
gateway_address.pattern_type = 'SINGLE'
gateway_address.single = '12.1.1.1'
gateway_address.update()

ipv4_source_address = icmp_redirect_frame_1.ipv4_source_address()
ipv4_source_address.pattern_type = 'INCREMENT'
ipv4_source_address.update()

ipv4_source_address_incr = ipv4_source_address.increment()
ipv4_source_address_incr.start = '10.10.10.10'
ipv4_source_address_incr.step = '0.0.0.2'
ipv4_source_address_incr.count = '2'
ipv4_source_address_incr.update()

ipv4_destination_address = icmp_redirect_frame_1.ipv4_destination_address()
ipv4_destination_address.pattern_type = 'SINGLE'
ipv4_destination_address.single = '20.20.20.20'
ipv4_destination_address.update()

reserved_bit = icmp_redirect_frame_1.ipv4_reserved_bit()
reserved_bit.pattern_type = 'SINGLE'
reserved_bit.single = '1'
reserved_bit.update()

ipv4_checksum = icmp_redirect_frame_1.ipv4_checksum()
ipv4_checksum.pattern_type = 'SINGLE'
ipv4_checksum.single = '100'
ipv4_checksum.update()

ipv4_df_bit = icmp_redirect_frame_1.ipv4_df_bit()
ipv4_df_bit.pattern_type = 'INCREMENT'
ipv4_df_bit.update()

ipv4_df_bit_incr = ipv4_df_bit.increment()
ipv4_df_bit_incr.start = '1'
ipv4_df_bit_incr.step = '1'
ipv4_df_bit_incr.count = '1'
ipv4_df_bit_incr.update()

print('\n  step 4. start traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.targets.append('Stream2')
traffic_control_input1.targets.append('Stream3')
traffic_control_input1.targets.append('Stream4')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

time.sleep(5)

print('\n  step 6. stop traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.targets.append('Stream2')
traffic_control_input1.targets.append('Stream3')
traffic_control_input1.targets.append('Stream4')
traffic_control_input1.mode = 'STOP'
config.traffic_control(traffic_control_input1)

print('\n  step 7. get statistics\n')
statistics = session.statistics()

statistics_traffic = statistics.port_traffic('Stream1')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

statistics_traffic = statistics.port_traffic('Stream3')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

statistics_traffic = statistics.port_traffic('Stream2')
print('%s \n' % statistics_traffic._values)
print('%s \n' % statistics_traffic.tx_frames)
print('%s \n' % statistics_traffic.rx_frames)

statistics_traffic = statistics.port_traffic('Stream4')
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
