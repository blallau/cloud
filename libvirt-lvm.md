
# 1 Overview

This guide is for building KVM hypervisor and VM.


# 2 Hypervisor

Ubuntu Trusty 14.04.5 or Xenial 16.04.3

A disk partition is required to be the volume pool for VMs.

## 2.1 Setup network

Install bridge-utils package.
```
apt-get install bridge-utils
```

Update /etc/network/interfaces.
```
# The loopback network interface
auto lo
iface lo inet loopback

auto eno1
iface eno1 inet manual

auto enp4s0f1
iface enp4s0f1 inet manual

auto br0
iface br0 inet static
    address 10.84.29.16
    netmask 255.255.255.0
    gateway 10.84.29.254
    bridge_ports eno1

dns-nameservers 10.84.5.100 172.21.200.60 172.29.131.60
dns-search contrail.juniper.net juniper.net englab.juniper.net

auto br1
iface br1 inet static
    address 192.168.2.16
    netmask 255.255.255.0
    bridge_ports enp4s0f1
    up ip route add 192.168.0.0/16 via 192.168.2.254
```

## 2.2 Install libvirt

```
apt-get install qemu-kvm libvirt-bin virtinst libguestfs-tools
```

## 2.3 Build volume pool
```
virsh pool-define-as --name lv --type logical --source-dev /dev/sdb
virsh pool-build lv
virsh pool-start lv
virsh pool-autostart lv
```

## 2.4 Update apparmor
Update /etc/apparmor.d/abstractions/libvirt-qemu to allow access to volume devices.
```
  network inet stream,
  network inet6 stream,

+ /dev/dm* rw,
  /dev/net/tun rw,
  /dev/tap* rw,
```

# 3 Launch VM

## 3.1 Create VM to boot from network

Create volume
```
virsh vol-create-as lv controller 150G
```

```
virt-install --connect qemu:///system --virt-type kvm \
    --name <vm name> --vcpus <cpu> --ram <MB> \
    --disk bus=virtio,vol=<pool>/<volume>,cache=none \
    -w bridge=<bridge>,model=virtio \
    --graphics vnc,listen=0.0.0.0 --noautoconsole \
    --pxe --boot network
```

## 3.2 Create VM based on CentOS cloud image

Create volume
```
virsh vol-create-as lv controller 150G
```

Extend cloud image to created volume.
```
virt-resize \
    /var/tmp/CentOS-7-x86_64-GenericCloud-1710.qcow2 \
    /dev/lv/controller \
    --expand /dev/sda1
```

Customize the image on volume.
```
virt-customize \
    -a /dev/lv/$name \
    --hostname $name \
    --root-password password:c0ntrail123 \
    --upload hosts:/etc \
    --run-command 'sed -i "s/#UseDNS yes/UseDNS no/g" /etc/ssh/sshd_config' \
    --run-command 'mkdir -p /root/.ssh' \
    --upload authorized_keys:/root/.ssh \
    --run-command 'chmod 600 /root/.ssh/authorized_keys' \
    --upload ifcfg-eth0:/etc/sysconfig/network-scripts \
    --upload ifcfg-eth1:/etc/sysconfig/network-scripts \
    --run-command 'yum remove -y cloud-init' \
    --run-command 'systemctl disable chronyd' \
    --install 'ntp' \
    --upload ntp.conf:/etc \
    --run-command 'systemctl enable ntpd' \
    --selinux-relabel
```

/etc/hosts 
```
127.0.0.1 localhost.contrail.juniper.net localhost
10.84.29.61 controller.contrail.juniper.net controller
```

/etc/ntp.conf 
```
driftfile /var/lib/ntp/drift
server 10.84.5.100
restrict 127.0.0.1
restrict -6 ::1
includefile /etc/ntp/crypto/pw
keys /etc/ntp/keys
```

/etc/sysconfig/network-scripts/ifcfg-eth0
```
DEVICE=eth0
TYPE=Ethernet
BOOTPROTO=static
ONBOOT=yes
IPADDR=10.84.29.61
NETMASK=255.255.255.0
GATEWAY=10.84.29.254
DNS1=10.84.5.100
DNS2=172.21.200.60
DOMAIN="contrail.juniper.net juniper.net englab.juniper.net"
```

/etc/sysconfig/network-scripts/ifcfg-eth1
```
DEVICE=eth1
TYPE=Ethernet
BOOTPROTO=static
ONBOOT=yes
IPADDR=192.168.2.61
NETMASK=255.255.255.0
```

Start VM.
```
virt-install --connect qemu:///system --virt-type kvm \
    --name $1 --vcpus 12 --ram 32768 \
    --disk bus=virtio,vol=lv/$name,cache=none \
    -w bridge=br0,model=virtio \
    -w bridge=br1,model=virtio \
    --graphics vnc,listen=0.0.0.0 --noautoconsole \
    --boot hd
```

## 3.3 Create VM based on Ubuntu cloud image


# 4 Volume

## 4.1 Attach disk

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


## 4.2 Volume backup and restore

Restore QCOW2 image to volume.
```
qemu-img convert -O raw cirros-0.3.4-x86_64-disk.img /dev/mapper/pool--lvm-vol--vm198
```

Backup volume to QCOW2 image.
```
qemu-img convert -O qcow2 /dev/mapper/pool--lvm-vol--vm198 cirros.qcow2
```
This process takes a while and QCOW2 image is big.


# 5 libguestfs-tools

Install libguestfs-tools.
```
apt-get install libguestfs-tools
```

```
# virt-df -h CentOS-7-x86_64-GenericCloud-1710.qcow2 
Filesystem                                Size       Used  Available  Use%
CentOS-7-x86_64-GenericCloud-1710.qcow2:/dev/sda1
                                          8.0G       795M       7.2G   10%

# virt-list-partitions CentOS-7-x86_64-GenericCloud-1710.qcow2 
/dev/sda1

# virt-filesystems -l -a CentOS-7-x86_64-GenericCloud-1710.qcow2 
Name       Type        VFS  Label  Size        Parent
/dev/sda1  filesystem  xfs  -      8588886016  -

# virt-df xenial-server-cloudimg-i386-disk1.img 
Filesystem                           1K-blocks       Used  Available  Use%
xenial-server-cloudimg-i386-disk1.img:/dev/sda1
                                       2166272     809488    1340400   38%

# virt-list-partitions xenial-server-cloudimg-i386-disk1.img
/dev/sda1

# virt-filesystems -l -a xenial-server-cloudimg-i386-disk1.img 
Name       Type        VFS   Label            Size        Parent
/dev/sda1  filesystem  ext4  cloudimg-rootfs  2359296000  -
```


# Appendix

On Ubuntu Xenial, need to apply this patch manually. https://github.com/libguestfs/libguestfs/commit/fd60be95091a1923e108f72caf251f5549eeccd0

Patch the file and clean up existing guestfs.
```
cd /usr/lib/x86_64-linux-gnu/guestfs/supermin.d
tar xzf init.tar.gz
# patch
rm init.tar.gz
tar -cf init.tar init
gizp init.tar
rm -fr /var/tmp/.guestfs-*
```

```
@@ -109,6 +109,7 @@
 
 if test "$guestfs_network" = 1; then
     iface=$(ls -I all -I default -I lo /proc/sys/net/ipv4/conf)
+    touch /etc/fstab
     if dhclient --version >/dev/null 2>&1; then
         dhclient $iface
     else
```

