# test stpes:
#  1. create and connect two ports

from openhltspirent import Openhltest
import time
import sys

QEMU_DBG = False

#Commandline arguments
serverip=sys.argv[1]
chassisip=sys.argv[2]
sessionname=sys.argv[3]
portnumber=sys.argv[4]

if chassisip == '0.0.0.0':
    QEMU_DBG = True

if QEMU_DBG:
    chassisip_1 = '10.61.67.21'
    chassisip_2 = '10.61.67.81'

print("ohtweb server ip", serverip)
if QEMU_DBG:
    print("chassis ip", chassisip_1, chassisip_2)
else:    
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

port1 = config.create_ports('Eth1')
if QEMU_DBG:
    port1.location = chassisip_1 + r'/1/1'
else:
    port1.location = chassisip + r'/1/1'
port1.update()

port2 = config.create_ports('Eth2')
if QEMU_DBG:
    port2.location = chassisip_2 + r'/1/1'
else:    
    port2.location = chassisip + r'/1/2'
port2.update()

port_control_input = config.PortControlInput()
port_control_input.targets = ['Eth1', 'Eth2']
port_control_input.mode = 'CONNECT'
config.port_control(port_control_input)

#  step 2. create one devices under the port1, protocol stack: eth/vlan/vlan/ipv4/dhcpv4. 
print('\n  step 2. create two devices under the port1, protocol stack: eth/ipv4/dhcpv4.\n')
# create device groups: 'Device group 1' under the port 'Eth1'
device_group_1 = config.create_device_groups('DeviceGroup1')
device_group_1.ports = ['Eth1']
device_group_1.update()

# create devices: 'Devices 1' under the device_group_east
devices_1 = device_group_1.create_devices('Device1')

#set device count
devices_1.device_count_per_port = 1
devices_1.update()

# create protocols ethernet
protocol_eth_1 = devices_1.create_protocols('EthIf')
protocol_eth_1.protocol_type = 'ETHERNET'
protocol_eth_1.update()

# create protocols IPv4
protocol_ipv4_1 = devices_1.create_protocols('IPv4If')
protocol_ipv4_1.protocol_type = 'IPV4'
protocol_ipv4_1.parent_link = 'EthIf'
protocol_ipv4_1.update()

# config mac addr
eth_1 = protocol_eth_1.ethernet()
eth_1.update()

eth_1_mac = eth_1.mac()
eth_1_mac.pattern_type = 'SINGLE'
eth_1_mac.single = '00:10:94:00:00:02'
eth_1_mac.update()

# config ipv4 address
ipv4_1 = protocol_ipv4_1.ipv4()
ipv4_1.update()

ipv4_1_src_addr = ipv4_1.source_address()
ipv4_1_src_addr.pattern_type = 'SINGLE'
ipv4_1_src_addr.single = '10.10.10.2'
ipv4_1_src_addr.update()

ipv4_1_gw_addr = ipv4_1.gateway_address()
ipv4_1_gw_addr.pattern_type = 'SINGLE'
ipv4_1_gw_addr.single = '10.10.10.1'
ipv4_1_gw_addr.update()

#create and config DHCPv4 client protocol
protocol_dhcpv4_1 = devices_1.create_protocols('DHCPV4_1')
protocol_dhcpv4_1.protocol_type = 'DHCPV4'
protocol_dhcpv4_1.parent_link = 'IPv4If'
protocol_dhcpv4_1.update()

dhcpv4_1 = protocol_dhcpv4_1.dhcpv4()
dhcpv4_1.update()

session_host_name = dhcpv4_1.session_host_name()
session_host_name.pattern_type = 'SINGLE'
session_host_name.single = 'dhcpv41'
session_host_name.update()

default_host_address_prefix_length = dhcpv4_1.default_host_address_prefix_length()
default_host_address_prefix_length.pattern_type = 'SINGLE'
default_host_address_prefix_length.single = '16'
default_host_address_prefix_length.update()

enable_arp_server_id = dhcpv4_1.enable_arp_server_id()
enable_arp_server_id.pattern_type = 'SINGLE'
enable_arp_server_id.single = 'false'
enable_arp_server_id.update()

enable_auto_retry = dhcpv4_1.enable_arp_server_id()
enable_auto_retry.pattern_type = 'SINGLE'
enable_auto_retry.single = 'true'
enable_auto_retry.update()

auto_retry_attempts = dhcpv4_1.auto_retry_attempts()
auto_retry_attempts.pattern_type = 'SINGLE'
auto_retry_attempts.single = '3'
auto_retry_attempts.update()

enable_broadcast_flag = dhcpv4_1.enable_broadcast_flag()
enable_broadcast_flag.pattern_type = 'SINGLE'
enable_broadcast_flag.single = 'false'
enable_broadcast_flag.update()

enable_client_mac_address_dataplane = dhcpv4_1.enable_client_mac_address_dataplane()
enable_client_mac_address_dataplane.pattern_type = 'SINGLE'
enable_client_mac_address_dataplane.single = 'false'
enable_client_mac_address_dataplane.update()

enable_router_option = dhcpv4_1.enable_router_option()
enable_router_option.pattern_type = 'SINGLE'
enable_router_option.single = 'false'
enable_router_option.update()

tos = dhcpv4_1.tos()
tos.pattern_type = 'SINGLE'
tos.single = '192'
tos.update()

#  step 3. create one devices under the port2, protocol stack: eth/ipv4/dhcpv4_server. 
print('\n  step 3. create one devices under the port2, protocol stack: eth/ipv4/dhcpv4_server.\n')
# create device groups: 'Device group 1' under the port 'Eth1'
device_group_2 = config.create_device_groups('DeviceGroup2')
device_group_2.ports = ['Eth2']
device_group_2.update()

# create devices: 'Devices 2' under the device_group_east
devices_2 = device_group_2.create_devices('Device2')

#set device count
devices_2.device_count_per_port = 1
devices_2.update()

# create protocols ethernet
protocol_eth_2 = devices_2.create_protocols('EthIf')
protocol_eth_2.protocol_type = 'ETHERNET'
protocol_eth_2.update()

# create protocols IPv4
protocol_ipv4_2 = devices_2.create_protocols('IPv4If')
protocol_ipv4_2.protocol_type = 'IPV4'
protocol_ipv4_2.parent_link = 'EthIf'
protocol_ipv4_2.update()

# config mac addr
eth_2 = protocol_eth_2.ethernet()
eth_2.update()

eth_2_mac = eth_1.mac()
eth_2_mac.pattern_type = 'SINGLE'
eth_2_mac.single = '00:10:94:00:00:01'
eth_2_mac.update()

# config ipv4 address
ipv4_2 = protocol_ipv4_2.ipv4()
ipv4_2.update()

ipv4_2_src_addr = ipv4_2.source_address()
ipv4_2_src_addr.pattern_type = 'SINGLE'
ipv4_2_src_addr.single = '10.10.10.1'
ipv4_2_src_addr.update()

ipv4_2_gw_addr = ipv4_2.gateway_address()
ipv4_2_gw_addr.pattern_type = 'SINGLE'
ipv4_2_gw_addr.single = '10.10.10.2'
ipv4_2_gw_addr.update()

#create and config DHCPv4 client protocol
protocol_dhcpv4_server_2 = devices_2.create_protocols('DHCPV4_SERVER_1')
protocol_dhcpv4_server_2.protocol_type = 'DHCPV4_SERVER'
protocol_dhcpv4_server_2.parent_link = 'IPv4If'
protocol_dhcpv4_server_2.update()

dhcpv4_server_2 = protocol_dhcpv4_server_2.dhcpv4_server()
dhcpv4_server_2.update()

host_name = dhcpv4_server_2.host_name()
host_name.pattern_type = 'SINGLE'
host_name.single = 'dhcpv4server1'
host_name.update()

tos = dhcpv4_server_2.tos()
tos.pattern_type = 'SINGLE'
tos.single = '192'
tos.update()

assign_strategy = dhcpv4_server_2.assign_strategy()
assign_strategy.pattern_type = 'SINGLE'
assign_strategy.single = 'GATEWAY'
assign_strategy.update()

decline_reserve_time = dhcpv4_server_2.decline_reserve_time()
decline_reserve_time.pattern_type = 'SINGLE'
decline_reserve_time.single = '10'
decline_reserve_time.update()

default_server_address_pool = dhcpv4_server_2.default_server_address_pool()
default_server_address_pool.update()
start_ipv4_address = default_server_address_pool.start_ipv4_address()
start_ipv4_address.pattern_type = 'SINGLE'
start_ipv4_address.single = '10.10.10.10'
start_ipv4_address.update()

'''
#  step 4. create dhcpv4 global_protocols
print('\n  step 4. create dhcpv4 global_protocols the port1, port2.\n')
global_protocols = config.global_protocols()
dhcpv4global1 = global_protocols.create_dhcpv4('dhcpv4global1')
dhcpv4global1.ports = ['Eth1']
dhcpv4global1.update()
request_rate = dhcpv4global1.request_rate()
request_rate.pattern_type = 'SINGLE'
request_rate.single = '100'
request_rate.update()

dhcpv4global2 = global_protocols.create_dhcpv4('dhcpv4global2')
dhcpv4global2.ports = ['Eth2']
dhcpv4global2.update()
request_rate = dhcpv4global2.request_rate()
request_rate.pattern_type = 'SINGLE'
request_rate.single = '100'
request_rate.update()
'''

'''
#SaveAsxml
save_config_input = config.SaveInput()
save_config_input.file_data = 'd:\\ospfvs.xml'
save_config_input.mode = "VENDOR_BINARY"
config.save(save_config_input)
'''

#  step 5. start dhcpv4 server 
print('\n  step 5. start dhcpv4 server protocol\n')
dhcpv4_server_control_input = config.Dhcpv4ServerControlInput()
dhcpv4_server_control_input.mode = 'START'
dhcpv4_server_control_input.targets = ['DHCPV4_SERVER_1']
config.dhcpv4_server_control(dhcpv4_server_control_input)

time.sleep(5)

#  step 6. start dhcpv4 client 
print('\n  step 6. start dhcpv4 client protocol\n')
dhcpv4_control_input = config.Dhcpv4ControlInput()
dhcpv4_control_input.mode = 'BIND'
dhcpv4_control_input.targets = ['DHCPV4_1']
config.dhcpv4_control(dhcpv4_control_input)

time.sleep(10)

#  step 7. Get the DHCPv4 statistics
print('\n  step 7. Get the DHCPv4 statistics\n')
statistics = session.statistics()
dhcpv4_statistics = statistics.dhcpv4_statistics('Device1')
dhcpv4_server_statistics = statistics.dhcpv4_server_statistics('Device2')
print('\ndhcpv4_statistics: %s' %(dhcpv4_statistics._values))
print('\ndhcpv4_server_statistics: %s' %(dhcpv4_server_statistics._values))

current_bound_count = dhcpv4_server_statistics._values['current-bound-count']
if (current_bound_count == 1) :
    print('*' * 40)
    print ("\n Info :DHCPv4 session bind successful \n")
    print('*' * 40)
else :
    print ("\n <error> Failed to bind DHCPv4 session \n")

#  step 8. disconnect ports
print('\n  step 8. Disconnect ports\n')
port_control_input = config.PortControlInput()
port_control_input.targets = ['Eth1', 'Eth2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

if QEMU_DBG == False:
    print('\n  step 9. delete session\n')
    session.delete()
