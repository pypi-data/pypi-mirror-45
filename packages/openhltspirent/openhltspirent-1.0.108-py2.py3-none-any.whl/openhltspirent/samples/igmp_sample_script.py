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

#  step 1. create and connect one ports
print('\n  step 1. create and connect one ports\n')
config = session.config()

port1 = config.create_ports('Eth1')
if QEMU_DBG:
    port1.location = chassisip_1 + r'/1/1'
else:
    port1.location = chassisip + r'/1/1'
port1.update()

port_control_input = config.PortControlInput()
port_control_input.targets = ['Eth1']
port_control_input.mode = 'CONNECT'
config.port_control(port_control_input)

#  step 2. create global multicast group
print('\n  step 2. create global multicast group\n')
global_multicast_groups = config.create_global_multicast_groups('globalmulticastgroupconfig1')
global_multicast_groups.update()
multicast_groups = global_multicast_groups.create_multicast_groups('Ipv4Group1')
multicast_groups.number_of_groups = '1'
multicast_groups.group_type = 'IPV4'
multicast_groups.update()

ipv4_group = multicast_groups.ipv4_group()
address = ipv4_group.address()
address.pattern_type = 'INCREMENT'
address.update()
increament = address.increment()
increament.start = '225.0.0.1'
increament.step = '1'
increament.count = '100'
increament.update()

#  step 3. create one devices under the port1, protocol stack: eth/vlan/vlan/ipv4/dhcpv4. 
print('\n  step 3. create two devices under the port1, protocol stack: eth/ipv4/dhcpv4.\n')
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

#create and config IGMP client protocol
protocol_igmp_1 = devices_1.create_protocols('IGMP_1')
protocol_igmp_1.protocol_type = 'IGMP'
protocol_igmp_1.parent_link = 'IPv4If'
protocol_igmp_1.update()

igmp_1 = protocol_igmp_1.igmp()
igmp_1.multicast_group = ['Ipv4Group1']
#igmp_1.multicast_group = ['globalmulticastgroupconfig1']
igmp_1.update()

version = igmp_1.version()
version.pattern_type = 'SINGLE'
version.single = 'IGMP_V1'
version.update()

force_leave = igmp_1.force_leave()
force_leave.pattern_type = 'SINGLE'
force_leave.single = 'true'
force_leave.update()

#  step 4. start igmp
print('\n  step 4. start igmp protocol\n')
igmp_control_input = config.IgmpControlInput()
igmp_control_input.mode = 'JOIN'
igmp_control_input.targets = ['IGMP_1']
igmp_control_input.calculate_latency = 'false'
igmp_control_input.join_failed_retry_counter = '0'
igmp_control_input.join_leave_delay = '0'
igmp_control_input.rx_data_duration = '10'
config.igmp_control(igmp_control_input)

time.sleep(10)

#  step 5. Get the igmp statistics
print('\n  step 5. Get the IGMP statistics\n')
statistics = session.statistics()
igmp_statistics = statistics.igmp_statistics('Device1')
print(igmp_statistics._values)

current_bound_count = igmp_statistics._values['tx-frame-count']
if (current_bound_count == 200) :
    print('*' * 40)
    print ("\n Info :IGMP session bind successful \n")
    print('*' * 40)
else :
    print ("\n <error> Failed to bind IGMP session \n")

#  step 6. disconnect ports
print('\n  step 6. Disconnect ports\n')
port_control_input = config.PortControlInput()
port_control_input.targets = ['Eth1']
port_control_input.mode = 'DISCONNECT'
config.port_control(port_control_input)

if QEMU_DBG == False:
    print('\n  step 7. delete session\n')
    session.delete()