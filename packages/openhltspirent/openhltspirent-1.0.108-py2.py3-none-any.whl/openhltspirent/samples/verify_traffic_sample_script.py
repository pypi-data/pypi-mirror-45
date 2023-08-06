from __future__ import print_function
from openhltspirent import Openhltest
import time
import sys
import json

step = 0

def printStep(msg):
    global step
    step += 1
    print('\n  step ' + str(step) +'. '+ str(msg) +'\n')

def pprint_output(output):
    print("\npretty print:")
    for table in ["item-table", "flow-table"]:
        if table in output["openhltest:output"]:
            print(table, ":")
            print(output["openhltest:output"][table])

    for stats in ["item-stats", "flow-stats"]:
        if stats in output["openhltest:output"]:
            print(stats, ":")
            print(json.dumps(output["openhltest:output"][stats], indent=4))

# Commandline arguments
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
printStep("Create and connect two ports")
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

################### create raw streamblocks ###################
print('\nCreate Raw Steramblock\n')
printStep('Create ipv4 raw streamblock')
port_traffic_1 = config.create_port_traffic('IPV4Stream1_raw')
port_traffic_1.source = 'Ethernet1'
port_traffic_1.update()

printStep('Create ipv6 raw streamblock')
# create IPv6 raw streamblock
port_traffic_2 = config.create_port_traffic('IPV6Stream1_raw')
port_traffic_2.source = 'Ethernet2'
port_traffic_2.update()

################### create bound streamblocks ###################
print('\nCreate Bound Steramblock\n')
printStep('Create devices under the port1, protocol stack: eth/ipv4.\n')
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

# create protocols IPv4
protocol_ipv4_1 = devices_1.create_protocols('IPV41')
protocol_ipv4_1.protocol_type = 'IPV4'
protocol_ipv4_1.parent_link = 'Ethernet1'
protocol_ipv4_1.update()

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

printStep('Create two devices under the port2, protocol stack: eth/ipv4.')

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

# create protocol IPv4
protocol_ipv4_2 = devices_2.create_protocols('IPV42')
protocol_ipv4_2.protocol_type = 'IPV4'
protocol_ipv4_2.parent_link = 'Ethernet2'
protocol_ipv4_2.update()

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


printStep('Create devices under the port1, protocol stack: eth/ipv6.')
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

# create protocols IPv6
protocol_ipv6_1 = devices_3.create_protocols('IPV61')
protocol_ipv6_1.protocol_type = 'IPV6'
protocol_ipv6_1.parent_link = 'Ethernet3'
protocol_ipv6_1.update()

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

printStep('Create two devices under the port2, protocol stack: eth/ipv6.')

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

# create protocol IPv6
protocol_ipv6_2 = devices_4.create_protocols('IPV62')
protocol_ipv6_2.protocol_type = 'IPV6'
protocol_ipv6_2.parent_link = 'Ethernet4'
protocol_ipv6_2.update()

# config ipv6 address
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
device_traffic_1 = config.create_device_traffic('IPV4Stream1_bound')

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


# create BOUND streamblock - IPv6 endpoints
device_traffic_2 = config.create_device_traffic('IPV6Stream1_bound')

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


################### create bound streamblocks end ###################

printStep("Start traffic")
traffic_control_input1 = config.TrafficControlInput()
traffic_control_input1.targets.append('IPV4Stream1_raw')
traffic_control_input1.targets.append('IPV6Stream1_raw')
traffic_control_input1.targets.append('IPV4Stream1_bound')
traffic_control_input1.targets.append('IPV6Stream1_bound')
traffic_control_input1.mode = 'START'
config.traffic_control(traffic_control_input1)

time.sleep(5)

## save configuration 
printStep("Save xml")
save_config_input = config.SaveInput()
save_config_input.file_name = ''
save_config_input.mode = "VENDOR_BINARY"
config.save(save_config_input)

# Verify traffic during running
printStep("Verify traffic during running #1")

verify_traffic_input1 = config.VerifyTrafficInput(tolerance=1, verify_mode='dropped_frames', debug=True, save_db=True)
traffic_items = verify_traffic_input1.create_traffic_items(all_traffic_items=False)
traffic_item_spec1 = traffic_items.create_traffic_item_spec("IPV4Stream1_raw")
traffic_items.traffic_item_spec.append(traffic_item_spec1)
traffic_item_spec2 = traffic_items.create_traffic_item_spec("IPV6Stream1_raw")
traffic_items.traffic_item_spec.append(traffic_item_spec2)
traffic_item_spec3 = traffic_items.create_traffic_item_spec("IPV4Stream1_bound")
traffic_items.traffic_item_spec.append(traffic_item_spec3)
traffic_item_spec4 = traffic_items.create_traffic_item_spec("IPV6Stream1_bound")
traffic_items.traffic_item_spec.append(traffic_item_spec4)
verify_traffic_input1.traffic_items = traffic_items

output = config.verify_traffic(verify_traffic_input1)

pprint_output(output)

# Verify traffic during running
printStep("Verify traffic during running #2")
verify_traffic_input1 = config.VerifyTrafficInput(tolerance=1, debug=True, save_db=False)
traffic_items = verify_traffic_input1.create_traffic_items(all_traffic_items=True)
verify_traffic_input1.traffic_items = traffic_items

output = config.verify_traffic(verify_traffic_input1)

pprint_output(output)


# Verify traffic during running
printStep("Verify traffic during running #3")
verify_traffic_input1 = config.VerifyTrafficInput(mode='rx_port', tolerance='100000', tolerance_mode='frame', debug=False, save_db=False)
traffic_items = verify_traffic_input1.create_traffic_items(all_traffic_items=False)
traffic_item_spec1 = traffic_items.create_traffic_item_spec("IPV4Stream1_bound")
traffic_items.traffic_item_spec.append(traffic_item_spec1)
verify_traffic_input1.traffic_items = traffic_items

ports = verify_traffic_input1.create_ports(all_ports=True)
verify_traffic_input1.ports = ports

output = config.verify_traffic(verify_traffic_input1)

pprint_output(output)

printStep("Verify traffic during running #4")
verify_traffic_input1 = config.VerifyTrafficInput(mode='rx_port', tolerance=1, debug=True, save_db=False)
traffic_items = verify_traffic_input1.create_traffic_items(all_traffic_items=False)
traffic_item_spec1 = traffic_items.create_traffic_item_spec("IPV4Stream1_raw")
traffic_items.traffic_item_spec.append(traffic_item_spec1)
traffic_item_spec4 = traffic_items.create_traffic_item_spec("IPV6Stream1_bound")
traffic_items.traffic_item_spec.append(traffic_item_spec4)
verify_traffic_input1.traffic_items = traffic_items

ports = verify_traffic_input1.create_ports(all_ports=True)
port_spec1 = ports.create_port_spec("IPV4Stream1_raw")
port_spec1.expected = '90'
port_stream_spec1 = port_spec1.create_port_stream_spec("Ethernet2")
port_stream_spec1.expected = '95'

port_stream_spec2 = port_spec1.create_port_stream_spec("Ethernet1")
port_stream_spec2.expected = '91'

port_spec1.port_stream_spec.append(port_stream_spec1)
port_spec1.port_stream_spec.append(port_stream_spec2)


port_spec2 = ports.create_port_spec("IPV6Stream1_bound")
port_spec2.expected = '70'
port_stream_spec3 = port_spec2.create_port_stream_spec("Ethernet2")
port_stream_spec3.expected = '75'

port_stream_spec4 = port_spec2.create_port_stream_spec("Ethernet1")
port_stream_spec4.expected = '75'

port_spec2.port_stream_spec.append(port_stream_spec3)
port_spec2.port_stream_spec.append(port_stream_spec4)

ports.port_spec.append(port_spec1)
ports.port_spec.append(port_spec2)
verify_traffic_input1.ports = ports

output = config.verify_traffic(verify_traffic_input1)

pprint_output(output)

# Stop traffic
printStep("Stop traffic")
traffic_control_input2 = config.TrafficControlInput()
traffic_control_input2.targets.extend(['IPV4Stream1_raw', 'IPV6Stream1_raw', 'IPV4Stream1_bound', 'IPV6Stream1_bound'])
traffic_control_input2.mode = 'STOP'
config.traffic_control(traffic_control_input2)


# Verify traffic after stop
printStep("Verify traffic after stop #5")

verify_traffic_input1 = config.VerifyTrafficInput(tolerance=3.2, mode='tx_port', debug=True, flow_per_stream=10, save_db=True)
traffic_items = verify_traffic_input1.create_traffic_items(all_traffic_items=False)
traffic_item_spec1 = traffic_items.create_traffic_item_spec("IPV4Stream1_bound")
traffic_items.traffic_item_spec.append(traffic_item_spec1)
traffic_item_spec2 = traffic_items.create_traffic_item_spec("IPV6Stream1_bound")
traffic_items.traffic_item_spec.append(traffic_item_spec2)
verify_traffic_input1.traffic_items = traffic_items

ports = verify_traffic_input1.create_ports(all_ports=False)
port_spec1 = ports.create_port_spec("Ethernet1")
ports.port_spec.append(port_spec1)
verify_traffic_input1.ports = ports

output = config.verify_traffic(verify_traffic_input1)
pprint_output(output)

printStep("Verify traffic after stop #6")

verify_traffic_input1 = config.VerifyTrafficInput(tolerance=3.2, expected='100', debug=False, flow_per_stream=10, save_db=True)
traffic_items = verify_traffic_input1.create_traffic_items(all_traffic_items=False)
traffic_item_spec1 = traffic_items.create_traffic_item_spec("IPV4Stream1_raw")
traffic_items.traffic_item_spec.append(traffic_item_spec1)
traffic_item_spec2 = traffic_items.create_traffic_item_spec("IPV6Stream1_raw")
traffic_items.traffic_item_spec.append(traffic_item_spec2)
verify_traffic_input1.traffic_items = traffic_items

output = config.verify_traffic(verify_traffic_input1)
pprint_output(output)

#disconnect ports
printStep('Disconnect ports')
port_control_input = config.PortControlInput()
port_control_input.targets = ['Ethernet1', 'Ethernet2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

printStep('Delete session')
session.delete()

