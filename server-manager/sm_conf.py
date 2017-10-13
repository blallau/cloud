
ntp_server = '10.84.5.100'
dns_server = '10.84.5.100 172.21.200.60 172.29.131.60'
dns_search = 'contrail.juniper.net juniper.net jnpr.net'
subnet = {
    '10.87.68.128': {
         'netmask': '255.255.255.128',
         'prefix-len': 25,
         'gateway': '10.87.68.254'},
    '10.84.29.0': {
         'netmask': '255.255.255.0',
         'prefix-len': 24,
         'gateway': '10.84.29.254'},
    '10.84.32.0': {
         'netmask': '255.255.255.128',
         'prefix-len': 25,
         'gateway': '10.84.32.126'},
    '172.16.0.0': {
         'netmask': '255.255.255.0',
         'prefix-len': 24,
         'gateway': '172.16.0.254'}}
vm_spec = {
    'sm': {'cpu': 2, 'memory': 16, 'disk': 100},
    'large': {'cpu': 6, 'memory': 64, 'disk': 100},
    'medium': {'cpu': 4, 'memory': 32, 'disk': 80},
    'small': {'cpu': 2, 'memory': 16, 'disk': 60}}
username = 'root'
password = 'c0ntrail123'

cluster_list = \
[
    {
        'name': 'poc1',
        'server': ['5b4-vm150', '5b4-vm151', '5b4-vm152',
                   '5b4-vm155', '5b4-vm156'],
        'image': 'ubuntu-16.04.2-vm-tony'},
    {
        'name': 'poc2',
        'server': ['5b4-vm160', '5b4-vm161'],
        'image': 'ubuntu-16.04.2-vm-tony'}
]

server_list = \
[
    {
        'hostname': '5b4s31',
        'type': 'kvm',
        'vol-pool': {
            'name': 'lvm',
            'device': '/dev/sda3'},
        'mgmt-if': {
            'name': 'em1',
            'bridge': 'br-mgmt',
            'address': '10.87.68.131',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'bond0',
            'bridge': 'br-data',
            'address': '172.16.0.131',
            'subnet': '172.16.0.0',
            'slave': ['p514p1', 'p514p2']}},
    {
        'hostname': '5b4s32',
        'type': 'kvm',
        'vol-pool': {
            'name': 'lvm',
            'device': '/dev/sda3'},
        'mgmt-if': {
            'name': 'em1',
            'bridge': 'br-mgmt',
            'address': '10.87.68.132',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'bond0',
            'bridge': 'br-data',
            'address': '172.16.0.132',
            'subnet': '172.16.0.0',
            'slave': ['p514p1', 'p514p2']}},
    {
        'hostname': '5b4s33',
        'type': 'kvm',
        'vol-pool': {
            'name': 'lvm',
            'device': '/dev/sda3'},
        'mgmt-if': {
            'name': 'em1',
            'bridge': 'br-mgmt',
            'address': '10.87.68.133',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'bond0',
            'bridge': 'br-data',
            'address': '172.16.0.133',
            'subnet': '172.16.0.0',
            'slave': ['p514p1', 'p514p2']}},
    {
        'hostname': '5b4s34',
        'type': 'bare',
        'mgmt-if': {
            'name': 'em1',
            'address': '10.87.68.134',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'bond0',
            'address': '172.16.0.134',
            'subnet': '172.16.0.0',
            'slave': ['p514p1', 'p514p2']}},
    {
        'hostname': '5b4s35',
        'type': 'bare',
        'mgmt-if': {
            'name': 'em1',
            'address': '10.87.68.135',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'bond0',
            'address': '172.16.0.135',
            'subnet': '172.16.0.0',
            'slave': ['p514p1', 'p514p2']}},
    {
        'hostname': '5b4s36',
        'type': 'kvm',
        'vol-pool': {
            'name': 'lvm',
            'device': '/dev/sda3'},
        'mgmt-if': {
            'name': 'em1',
            'bridge': 'br-mgmt',
            'address': '10.87.68.136',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'bond0',
            'bridge': 'br-data',
            'address': '172.16.0.136',
            'subnet': '172.16.0.0',
            'slave': ['p514p1', 'p514p2']}},
    {
        'hostname': '5b4s37',
        'type': 'kvm',
        'vol-pool': {
            'name': 'pool-lvm',
            'device': '/dev/sda3'},
        'mgmt-if': {
            'name': 'em1',
            'address': '10.87.68.137',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'bond0',
            'address': '172.16.0.137',
            'subnet': '172.16.0.0',
            'slave': ['p514p1', 'p514p2']}},
    {
        'hostname': 'a5s167',
        'type': 'bare',
        'mgmt-if': {
            'name': 'p1p1',
            'address': '10.84.32.12',
            'subnet': '10.84.32.0'}},
    {
        'hostname': 'a5s168',
        'type': 'bare',
        'mgmt-if': {
            'name': 'p1p1',
            'address': '10.84.32.13',
            'subnet': '10.84.32.0'}},
    {
        'hostname': '5b4-vm150',
        'type': 'vm',
        'hypervisor': '5b4s31',
        'spec': 'small',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.150',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.150',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm151',
        'type': 'vm',
        'hypervisor': '5b4s31',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.151',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.151',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm152',
        'type': 'vm',
        'hypervisor': '5b4s31',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.152',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.152',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm153',
        'type': 'vm',
        'hypervisor': '5b4s31',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.153',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.153',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm154',
        'type': 'vm',
        'hypervisor': '5b4s31',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.154',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.154',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm155',
        'type': 'vm',
        'hypervisor': '5b4s32',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.155',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.155',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm156',
        'type': 'vm',
        'hypervisor': '5b4s32',
        'spec': 'medium',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.156',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.156',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm157',
        'type': 'vm',
        'hypervisor': '5b4s32',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.157',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.157',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm158',
        'type': 'vm',
        'hypervisor': '5b4s32',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.158',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.158',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm159',
        'type': 'vm',
        'hypervisor': '5b4s32',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.159',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.159',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm160',
        'type': 'vm',
        'hypervisor': '5b4s33',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.160',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.160',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm161',
        'type': 'vm',
        'hypervisor': '5b4s33',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.161',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.161',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm162',
        'type': 'vm',
        'hypervisor': '5b4s33',
        'spec': 'large',
        'mgmt-if': {
            'name': 'ens3',
            'address': '10.87.68.162',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'ens4',
            'address': '172.16.0.162',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4-vm165',
        'type': 'vm',
        'hypervisor': '5b4s37',
        'spec': 'sm',
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.165',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.165',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s37-vm166',
        'type': 'vm',
        'spec': 'large',
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.166',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.166',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s37-vm167',
        'type': 'vm',
        'spec': 'large',
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.167',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.167',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s37-vm168',
        'type': 'vm',
        'spec': 'large',
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.168',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.168',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm170',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.170',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.170',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm171',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.171',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.171',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm172',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.172',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.172',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm173',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.173',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.173',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm174',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.174',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.174',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm175',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.175',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.175',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm176',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.176',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.176',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm177',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.177',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.177',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm178',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.178',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.178',
            'subnet': '172.16.0.0'}},
    {
        'hostname': '5b4s36-vm179',
        'type': 'vm',
        'cpu': 4,
        'memory': 32,
        'disk': 100,
        'mgmt-if': {
            'name': 'eth0',
            'address': '10.87.68.179',
            'subnet': '10.87.68.128'},
        'data-if': {
            'name': 'eth1',
            'address': '172.16.0.179',
            'subnet': '172.16.0.0'}},
]

