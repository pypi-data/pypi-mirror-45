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

#  step 2. create one devices under the port1, protocol stack: eth/vlan/vlan/ipv6/dhcpv6. 
print('\n  step 2. create two devices under the port1, protocol stack: eth/ipv6/dhcpv6.\n')
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

# create protocols IPv6
protocol_ipv6_1 = devices_1.create_protocols('IPv6If')
protocol_ipv6_1.protocol_type = 'IPV6'
protocol_ipv6_1.parent_link = 'EthIf'
protocol_ipv6_1.update()

# config mac addr
eth_1 = protocol_eth_1.ethernet()
eth_1.update()

eth_1_mac = eth_1.mac()
eth_1_mac.pattern_type = 'SINGLE'
eth_1_mac.single = '00:10:94:00:00:02'
eth_1_mac.update()

# config ipv6 address
ipv6_1 = protocol_ipv6_1.ipv6()
ipv6_1.update()

ipv6_1_src_addr = ipv6_1.source_address()
ipv6_1_src_addr.pattern_type = 'SINGLE'
ipv6_1_src_addr.single = '2001::1'
ipv6_1_src_addr.update()

ipv6_1_gw_addr = ipv6_1.gateway_address()
ipv6_1_gw_addr.pattern_type = 'SINGLE'
ipv6_1_gw_addr.single = '2001::3'
ipv6_1_gw_addr.update()

#create and config DHCPv6 client protocol
protocol_dhcpv6_1 = devices_1.create_protocols('DHCPV6_1')
protocol_dhcpv6_1.protocol_type = 'DHCPV6'
protocol_dhcpv6_1.parent_link = 'IPv6If'
protocol_dhcpv6_1.update()

dhcpv6_1 = protocol_dhcpv6_1.dhcpv6()
dhcpv6_1.update()

'''
session_host_name = dhcpv6_1.session_host_name()
session_host_name.pattern_type = 'SINGLE'
session_host_name.single = 'dhcpv61'
session_host_name.update()
'''

dhcpv6_client_mode = dhcpv6_1.dhcpv6_client_mode()
dhcpv6_client_mode.pattern_type = 'SINGLE'
dhcpv6_client_mode.single = 'DHCPV6'
dhcpv6_client_mode.update()

t1_timer = dhcpv6_1.t1_timer()
t1_timer.pattern_type = 'SINGLE'
t1_timer.single = '302400'
t1_timer.update()

t2_timer = dhcpv6_1.t2_timer()
t2_timer.pattern_type = 'SINGLE'
t2_timer.single = '483840'
t2_timer.update()

enable_renew = dhcpv6_1.enable_renew()
enable_renew.pattern_type = 'SINGLE'
enable_renew.single = 'true'
enable_renew.update()

interface_id = dhcpv6_1.interface_id()
interface_id.pattern_type = 'SINGLE'
interface_id.single = 'spirent'
interface_id.update()

#  step 3. create one devices under the port2, protocol stack: eth/ipv6/dhcpv6_server. 
print('\n  step 3. create one devices under the port2, protocol stack: eth/ipv6/dhcpv6_server.\n')
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

# create protocols IPv6
protocol_ipv6_2 = devices_2.create_protocols('IPv6If')
protocol_ipv6_2.protocol_type = 'IPV6'
protocol_ipv6_2.parent_link = 'EthIf'
protocol_ipv6_2.update()

# config mac addr
eth_2 = protocol_eth_2.ethernet()
eth_2.update()

eth_2_mac = eth_1.mac()
eth_2_mac.pattern_type = 'SINGLE'
eth_2_mac.single = '00:10:94:00:00:01'
eth_2_mac.update()

# config ipv6 address
ipv6_2 = protocol_ipv6_2.ipv6()
ipv6_2.update()

ipv6_2_src_addr = ipv6_2.source_address()
ipv6_2_src_addr.pattern_type = 'SINGLE'
ipv6_2_src_addr.single = '2001::3'
ipv6_2_src_addr.update()

ipv6_2_gw_addr = ipv6_2.gateway_address()
ipv6_2_gw_addr.pattern_type = 'SINGLE'
ipv6_2_gw_addr.single = '2001::1'
ipv6_2_gw_addr.update()

#create and config DHCPv6 client protocol
protocol_dhcpv6_server_2 = devices_2.create_protocols('DHCPV6_SERVER_1')
protocol_dhcpv6_server_2.protocol_type = 'DHCPV6_SERVER'
protocol_dhcpv6_server_2.parent_link = 'IPv6If'
protocol_dhcpv6_server_2.update()

dhcpv6_server_2 = protocol_dhcpv6_server_2.dhcpv6_server()
dhcpv6_server_2.update()

'''
host_name = dhcpv6_server_2.host_name()
host_name.pattern_type = 'SINGLE'
host_name.single = 'dhcpv6server1'
host_name.update()
'''

emulation_mode = dhcpv6_server_2.emulation_mode()
emulation_mode.pattern_type = 'SINGLE'
emulation_mode.single = 'DHCPV6'
emulation_mode.update()

preferred_lifetime = dhcpv6_server_2.preferred_lifetime()
preferred_lifetime.pattern_type = 'SINGLE'
preferred_lifetime.single = '504800'
preferred_lifetime.update()

server_address_pool = dhcpv6_server_2.server_address_pool()
server_address_pool.pattern_type = 'SINGLE'
server_address_pool.single = '2002::1'
server_address_pool.update()

'''
#SaveAsxml
save_config_input = config.SaveInput()
save_config_input.file_data = 'd:\\ospfvs.xml'
save_config_input.mode = "VENDOR_BINARY"
config.save(save_config_input)
'''

#  step 5. start dhcpv6 server 
print('\n  step 5. start dhcpv6 server protocol\n')
dhcpv6_server_control_input = config.Dhcpv6ServerControlInput()
dhcpv6_server_control_input.mode = 'START'
dhcpv6_server_control_input.targets = ['DHCPV6_SERVER_1']
config.dhcpv6_server_control(dhcpv6_server_control_input)

time.sleep(5)

#  step 6. start dhcpv6 client 
print('\n  step 6. start dhcpv6 client protocol\n')
dhcpv6_control_input = config.Dhcpv6ControlInput()
dhcpv6_control_input.mode = 'BIND'
dhcpv6_control_input.targets = ['DHCPV6_1']
config.dhcpv6_control(dhcpv6_control_input)

time.sleep(10)

#  step 7. Get the DHCPv6 statistics
print('\n  step 7. Get the DHCPv6 statistics\n')
statistics = session.statistics()
dhcpv6_statistics = statistics.dhcpv6_statistics('Device1')
dhcpv6_server_statistics = statistics.dhcpv6_server_statistics('Device2')
print('\ndhcpv6_statistics: %s' %(dhcpv6_statistics._values))
print('\ndhcpv6_server_statistics: %s' %(dhcpv6_server_statistics._values))

current_bound_count = dhcpv6_server_statistics._values['current-bound-count']
if (current_bound_count == 1) :
    print('*' * 40)
    print ("\n Info :DHCPv6 session bind successful \n")
    print('*' * 40)
else :
    print ("\n <error> Failed to bind DHCPv6 session \n")

#  step 8. disconnect ports
print('\n  step 8. Disconnect ports\n')
port_control_input = config.PortControlInput()
port_control_input.targets = ['Eth1', 'Eth2']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

if QEMU_DBG == False:
    print('\n  step 9. delete session\n')
    session.delete()
