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

#IGMP2 Report
frame_1 = port_traffic_1.create_frames('igmpv2_report')
frame_1.frame_type = 'IGMPV2_REPORT'
frame_1.update()

igmpv2_report_frame_1 = frame_1.igmpv2_report()
igmpv2_report_frame_1.update()

checksum = igmpv2_report_frame_1.checksum()
checksum.pattern_type = 'SINGLE'
checksum.single = '1000'
checksum.update()

group_address = igmpv2_report_frame_1.group_address()
group_address.pattern_type = 'SINGLE'
group_address.single = '255.0.0.10'
group_address.update()

max_response_time = igmpv2_report_frame_1.max_response_time()
max_response_time.pattern_type = 'INCREMENT'
max_response_time.update()

ipv4_source_address_incr = max_response_time.increment()
ipv4_source_address_incr.start = '10'
ipv4_source_address_incr.step = '2'
ipv4_source_address_incr.count = '2'
ipv4_source_address_incr.update()

print('\n  step 3. create ipv4 raw streamblock\n')
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
eth_src_addr_1_incr.count = '10'
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

#IGMP3 Report
frame_1 = port_traffic_2.create_frames('igmpv3_report')
frame_1.frame_type = 'IGMPV3_REPORT'
frame_1.update()

igmpv3_report_frame_1 = frame_1.igmpv3_report()
igmpv3_report_frame_1.update()

checksum = igmpv3_report_frame_1.checksum()
checksum.pattern_type = 'SINGLE'
checksum.single = '1000'
checksum.update()

group_address = igmpv3_report_frame_1.number_of_group_records()
group_address.pattern_type = 'SINGLE'
group_address.single = '10'
group_address.update()

reserved = igmpv3_report_frame_1.reserved()
reserved.pattern_type = 'INCREMENT'
reserved.update()

ipv4_source_address_incr = reserved.increment()
ipv4_source_address_incr.start = '10'
ipv4_source_address_incr.step = '2'
ipv4_source_address_incr.count = '2'
ipv4_source_address_incr.update()

reserved2 = igmpv3_report_frame_1.reserved2()
reserved2.pattern_type = 'SINGLE'
reserved2.single = '10'
reserved2.update()

print('\n  step 4. start traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.targets.append('Stream2')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

time.sleep(5)

print('\n  step 6. stop traffic\n')
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('Stream1')
traffic_control_input1.targets.append('Stream2')
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
