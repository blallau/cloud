
##1 Server

Ubuntu Trusty 14.04.5

A disk partition is required to be the volume pool for VMs.

###1.1 Setup network
Install bridge-utils package.
```
apt-get install bridge-utils
```

Update /etc/network/interfaces.
```
auto em1
iface em1 inet manual

auto br-mgmt
iface br-mgmt inet static
    address 10.87.64.146
    netmask 255.255.255.128
    gateway 10.87.64.254
    bridge_ports em1

dns-nameservers 10.84.5.100 8.8.8.8
dns-search juniper.net
```

###1.2 Install libvirt
```
apt-get install qemu-kvm libvirt-bin
```

##2 VM
###2.1 Build volume pool
```
virsh pool-define-as --name pool-lvm --type logical --source-dev /dev/sdb
virsh pool-build pool-lvm
virsh pool-start pool-lvm
virsh pool-autostart pool-lvm
```

###2.2 Create volume
```
virsh vol-create-as pool-lvm vol-vm198 60G
```

###2.3 Update apparmor
Update /etc/apparmor.d/abstractions/libvirt-qemu to allow access to volume devices.
```
  network inet stream,
  network inet6 stream,

+ /dev/dm* rw,
  /dev/net/tun rw,
  /dev/tap* rw,
```

###2.4 Launch VM
```
<domain type='kvm'>
  <name>vm198</name>
  <memory unit='G'>64</memory>
  <vcpu placement='static'>12</vcpu>
  <os>
    <type arch='x86_64'>hvm</type>
    <boot dev='network'/>
    <boot dev='hd'/>
  </os>
  <devices>
    <disk type='volume' device='disk'>
      <driver name='qemu' type='raw' cache='none'/>
      <source pool='pool-lvm' volume='vol-vm198'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='bridge'>
      <source bridge='br-mgmt'/>
      <model type='virtio'/>
    </interface>
    <serial type='pty'>
      <target port='0'/>
    </serial>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
    <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'>
      <listen type='address' address='0.0.0.0'/>
    </graphics>
  </devices>
</domain>
```

```
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2' cache='none'/>
      <source file='__image__'/>
      <target dev='vda' bus='virtio'/>
    </disk>
```

```
virt-install --connect qemu:///system --virt-type kvm \
    --name <vm name> --vcpus <cpu> --ram <MB> \
    --disk bus=virtio,vol=<pool>/<volume>,cache=none \
    -w bridge=<bridge>,model=virtio \
    --graphics vnc,listen=0.0.0.0 --noautoconsole \
    --pxe --boot network
```

##3 Attach disk
Create volume and attach to VM.
```
virsh vol-create-as pool-lvm vol-vm198-swap 64G
virsh attach-disk vm198 --source /dev/mapper/pool--lvm-vol--vm198--swap --target vdb --persistent
```

Reboot VM. Partition, format and mount new disk.
```
fdisk /dev/vdb
mkswap /dev/vdb1
swapon /dev/vdb1
```
Update /etc/fstab.
```
/dev/vdb1   swap            swap    defaults    0 0
```

For ext4 disk.
```
fdisk /dev/vdb
mkfs.ext4 /dev/vdb1
mkdir /mnt/new-disk
mount /dev/vdb1 /mnt/new-disk
```
Update /etc/fstab.
```
/dev/vdb1   /mnt/new-disk   ext4    defaults    0 0
```


##4 Volume backup and restore
Restore QCOW2 image to volume.
```
qemu-img convert -O raw cirros-0.3.4-x86_64-disk.img /dev/mapper/pool--lvm-vol--vm198
```

Backup volume to QCOW2 image.
```
qemu-img convert -O qcow2 /dev/mapper/pool--lvm-vol--vm198 cirros.qcow2
```
This process takes a while and QCOW2 image is big.


