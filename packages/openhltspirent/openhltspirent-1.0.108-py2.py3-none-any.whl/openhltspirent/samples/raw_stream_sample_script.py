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

eth_source_addr = ethernet_frame_1.source()
eth_source_addr.pattern_type = 'INCREMENT'
eth_source_addr.update()

eth_source_addr_incr = eth_source_addr.increment()
eth_source_addr_incr.start = '00:10:94:00:00:12'
eth_source_addr_incr.step = '00:00:00:00:00:02'
eth_source_addr_incr.count = '10'
eth_source_addr_incr.update()

eth_dest_addr = ethernet_frame_1.destination()
eth_dest_addr.pattern_type = 'SINGLE'
eth_dest_addr.single = '00:10:94:00:00:80'
eth_dest_addr.update()

# vlan
# Outer Vlan
frame_2 = port_traffic_1.create_frames('Vlan1')
frame_2.frame_type = 'VLAN'
frame_2.update()

vlan_frame_1 = frame_2.vlan()
vlan_frame_1.update()

vlan_id_1 = vlan_frame_1.id()
vlan_id_1.pattern_type = 'SINGLE'
vlan_id_1.single = '100'
vlan_id_1.update()

vlan_priority_1 = vlan_frame_1.priority()
vlan_priority_1.pattern_type = 'SINGLE'
vlan_priority_1.single = '3'
vlan_priority_1.update()


#Inner Vlan
frame_3 = port_traffic_1.create_frames('Vlan2')
frame_3.frame_type = 'VLAN'
frame_3.update()

vlan_frame_2 = frame_3.vlan()
vlan_frame_2.update()
vlan_id_2 = vlan_frame_2.id()
vlan_id_2.pattern_type = 'SINGLE'
vlan_id_2.single = '200'
vlan_id_2.update()

vlan_priority_2 = vlan_frame_2.priority()
vlan_priority_2.pattern_type = 'SINGLE'
vlan_priority_2.single = '6'
vlan_priority_2.update()

# # ipv4
frame_4 = port_traffic_1.create_frames('Ipv41')
frame_4.frame_type = 'IPV4'
frame_4.update()

ipv4_frame_1 = frame_4.ipv4()
ipv4_frame_1.update()

ipv4_source_addr = ipv4_frame_1.source_address()
ipv4_source_addr.pattern_type = 'VALUE_LIST'
ipv4_source_addr.value_list = ['1.1.1.1','2.2.2.2']
ipv4_source_addr.update()

ipv4_dest_addr = ipv4_frame_1.destination_address()
ipv4_dest_addr.pattern_type = 'SINGLE'
ipv4_dest_addr.single = '20.20.20.20'
ipv4_dest_addr.update()

ipv4_ttl = ipv4_frame_1.ttl()
ipv4_ttl.pattern_type = 'SINGLE'
ipv4_ttl.single = '243'
ipv4_ttl.update()

# tcp
frame_5 = port_traffic_1.create_frames('Tcp1')
frame_5.frame_type = 'TCP'
frame_5.update()

tcp_frame_1 = frame_5.tcp()
tcp_frame_1.update()
tcp_source_port = tcp_frame_1.source_port()
tcp_source_port.pattern_type = 'SINGLE'
tcp_source_port.single = '1111'
tcp_source_port.update()

tcp_dest_port = tcp_frame_1.destination_port()
tcp_dest_port.pattern_type = 'SINGLE'
tcp_dest_port.single = '2222'
tcp_dest_port.update()

tcp_checksum = tcp_frame_1.checksum()
tcp_checksum.pattern_type = 'SINGLE'
tcp_checksum.single =  '98'
tcp_checksum.update()

tcp_ack_num = tcp_frame_1.acknowledgement_number()
tcp_ack_num.pattern_type = 'SINGLE'
tcp_ack_num.single =  '234569'
tcp_ack_num.update()

tcp_header_length = tcp_frame_1.header_length()
tcp_header_length.pattern_type = 'SINGLE'
tcp_header_length.single =  '8'
tcp_header_length.update()

tcp_reserved = tcp_frame_1.reserved()
tcp_reserved.pattern_type = 'SINGLE'
tcp_reserved.single =  '33'
tcp_reserved.update()

tcp_sequence_number = tcp_frame_1.sequence_number()
tcp_sequence_number.pattern_type = 'SINGLE'
tcp_sequence_number.single =  '123455'
tcp_sequence_number.update()

tcp_urgent_pointer = tcp_frame_1.urgent_pointer()
tcp_urgent_pointer.pattern_type = 'SINGLE'
tcp_urgent_pointer.single =  '9'
tcp_urgent_pointer.update()

tcp_window_size = tcp_frame_1.window_size()
tcp_window_size.pattern_type = 'SINGLE'
tcp_window_size.single =  '2046'
tcp_window_size.update()

tcp_acknowledgement_flag = tcp_frame_1.acknowledgement_flag()
tcp_acknowledgement_flag.pattern_type = 'SINGLE'
tcp_acknowledgement_flag.single =  '0'
tcp_acknowledgement_flag.update()

tcp_fin_flag = tcp_frame_1.fin_flag()
tcp_fin_flag.pattern_type = 'SINGLE'
tcp_fin_flag.single =  '1'
tcp_fin_flag.update()

tcp_push_flag = tcp_frame_1.push_flag()
tcp_push_flag.pattern_type = 'SINGLE'
tcp_push_flag.single =  '1'
tcp_push_flag.update()

tcp_reset_flag = tcp_frame_1.reset_flag()
tcp_reset_flag.pattern_type = 'SINGLE'
tcp_reset_flag.single =  '1'
tcp_reset_flag.update()

tcp_sync_flag = tcp_frame_1.sync_flag()
tcp_sync_flag.pattern_type = 'SINGLE'
tcp_sync_flag.single =  '1'
tcp_sync_flag.update()

tcp_urgent_flag = tcp_frame_1.urgent_flag()
tcp_urgent_flag.pattern_type = 'SINGLE'
tcp_urgent_flag.single =  '1'
tcp_urgent_flag.update()
print('\n  step 3. create ipv6 raw streamblock\n')
# create IPv6 raw streamblock
port_traffic_2 = config.create_port_traffic('Stream2')
port_traffic_2.source = 'Ethernet2'
port_traffic_2.update()

#Config Frame Size
frame_length_1 = port_traffic_2.frame_length()
frame_length_1.length_type = 'FIXED'
frame_length_1.fixed = '256'
frame_length_1.update()

frame_1 = port_traffic_2.create_frames('Ethernet2')
frame_1.frame_type = 'ETHERNET'
frame_1.update()

# ethernet header
ethernet_frame_1 = frame_1.ethernet()
ethernet_frame_1.update()

eth_source_addr = ethernet_frame_1.source()
eth_source_addr.pattern_type = 'SINGLE'
eth_source_addr.single = '00:10:94:00:00:12'
eth_source_addr.update()

eth_dest_addr = ethernet_frame_1.destination()
eth_dest_addr.pattern_type = 'SINGLE'
eth_dest_addr.single = '00:10:94:00:00:23'
eth_dest_addr.update()

# vlan  

# Inner Vlan
frame_2 = port_traffic_2.create_frames('Vlan3')
frame_2.frame_type = 'VLAN'
frame_2.update()

vlan_frame_1 = frame_2.vlan()
vlan_frame_1.update()
vlan_id_1 = vlan_frame_1.id()
vlan_id_1.pattern_type = 'SINGLE'
vlan_id_1.single = '100'
vlan_id_1.update()

vlan_priority_1 = vlan_frame_1.priority()
vlan_priority_1.pattern_type = 'SINGLE'
vlan_priority_1.single = '3'
vlan_priority_1.update()

#Outer Vlan
frame_3 = port_traffic_2.create_frames('Vlan4')
frame_3.frame_type = 'VLAN'
frame_3.update()

vlan_frame_2 = frame_3.vlan()
vlan_frame_2.update()
vlan_id_2 = vlan_frame_2.id()
vlan_id_2.pattern_type = 'SINGLE'
vlan_id_2.single = '200'
vlan_id_2.update()

vlan_priority_2 = vlan_frame_2.priority()
vlan_priority_2.pattern_type = 'SINGLE'
vlan_priority_2.single = '6'
vlan_priority_2.update()

# # ipv6
frame_4 = port_traffic_2.create_frames('Ipv61')
frame_4.frame_type = 'IPV6'
frame_4.update()

ipv6_frame_1 = frame_4.ipv6()
ipv6_frame_1.update()

ipv6_source_addr = ipv6_frame_1.source_address()
ipv6_source_addr.pattern_type = 'INCREMENT'
ipv6_source_addr.update()

ipv6_source_addr_incr = ipv6_source_addr.increment()
ipv6_source_addr_incr.start = '3000::2'
ipv6_source_addr_incr.step = '::4'
ipv6_source_addr_incr.count = '13'
ipv6_source_addr_incr.update()


ipv6_dest_addr = ipv6_frame_1.destination_address()
ipv6_dest_addr.pattern_type = 'SINGLE'
ipv6_dest_addr.single = '4000::3'
ipv6_dest_addr.update()

# udp
frame_5 = port_traffic_2.create_frames('Udp1')
frame_5.frame_type = 'UDP'
frame_5.update()

udp_frame_1 = frame_5.udp()
udp_frame_1.update()


udp_source_port = udp_frame_1.source_port()
udp_source_port.pattern_type = 'SINGLE'
udp_source_port.singel = '1023'
udp_source_port.update()

udp_dst_port = udp_frame_1.destination_port()
udp_dst_port.pattern_type = 'SINGLE'
udp_dst_port.single = '1025'
udp_dst_port.update()

#SaveAsxml
save_config_input = config.SaveInput()
save_config_input.file_name = ''
save_config_input.mode = "VENDOR_BINARY"
config.save(save_config_input)


print('\n  step 4. start traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.targets.append('Stream2')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

#time.sleep(5)
#print('\n  step 6. stop traffic\n')
#traffic_control_input1 = config.TrafficControlInput()
#traffic_control_input1.targets.append('Stream1')
#traffic_control_input1.targets.append('Stream2')
#traffic_control_input1.mode = 'STOP'
#config.traffic_control(traffic_control_input1)


print('\n  step 7. get statistics\n')
statistics = session.statistics()
print(statistics._values)
statistics.port_traffic = statistics.port_traffic('Stream1')
print('%s \n' % statistics.port_traffic._values)

print('%s \n' % statistics.port_traffic.tx_frames)

statistics_traffic = statistics.port('Ethernet1')
print('%s \n' % statistics_traffic._values)

print('%s \n' % statistics_traffic.tx_frames)


statistics = session.statistics()
print(statistics._values)
statistics.port_traffic = statistics.port_traffic('Stream2')
print('%s \n' % statistics.port_traffic._values)

print('%s \n' % statistics.port_traffic.tx_frames)

statistics_traffic = statistics.port('Ethernet2')
print('%s \n' % statistics_traffic._values)

print('%s \n' % statistics_traffic.tx_frames)


print('\n  step 8. stop traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.targets.append('Stream2')
traffic_control_input1.mode = 'STOP'
config.traffic_control(traffic_control_input1)

#disconnect ports
port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

print('\n  step 9. delete session\n')
session.delete()
