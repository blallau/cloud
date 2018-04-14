# Mount

modprobe nbd max_part=63
qemu-nbd -c /dev/nbd0 image.img
mount /dev/nbd0p1 /mnt

umount /mnt
qemu-nbd -d /dev/nbd0
rmmod nbd

Update /etc/ssh/sshd_config.
```
PermitRootLogin yes
#PasswordAuthentication yes
```

Update /etc/cloud/cloud.cfg.d/90_dpkg.cfg, set datasource_list to None.


# Mounting and Modifying Virtual Disk Images

If you use KVM virtual machines in your Linux environment, you may want to mount and examine or modify the contents of a partition on a virtual disk.  Here's one way to do it.


## Getting to Partitions on QCOW2 Images

This condensed recipe applies to qcow2 disk images.  The image partitions can be mounted on the host for read/write access using QEMUs Network Block Device (NBD) server.

The VM should be down for this procedure.

First, check to see that you have available /dev/nbd devices.  Depending on how many you need, you can create more:
```
modprobe nbd max_part=16
```

Export the image and look for partitions.  Use the full path name to the image.
```
qemu-nbd -c /dev/nbd0 /var/lib/libvirt/images/testbox.img
```

You may need to probe for partitions but I haven't had to.  
```
partprobe /dev/nbd0
```

The qemu-nbd command will create an nbd device for each partition.  For example, /dev/nbd0p1.  You can try to mount one of these partitions now but, if the disk image belongs to a Linux guest, it may fail.  Mount can't work directly with LVM partitions.
```
mount /dev/nbd0p1 /mnt/qemu/p1
mount: unknown filesystem type 'LVM2_member'
```

See the section "Mounting Logical Volumes" below for that procedure.

Once you've finished with the image, reverse the order of the steps above.  I don't know if it's actually necessary to deactivate the volume group, but you definitely should "disconnect" the QEMU block device after unmounting the partition:
```
qemu-nbd -d /dev/nbd0
```

Getting to Partitions on Raw Images
Raw disk images are just that: a binary disk image in a file.  You can see the partitions with fdisk:
```
# fdisk -l /path/to/disk.img
Disk disk.img: 10.7 GB, 10737418240 bytes
255 heads, 63 sectors/track, 1305 cylinders, total 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00068f41

   Device Boot      Start         End      Blocks   Id  System
disk.img1   *        2048     1026047      512000   83  Linux
disk.img2         1026048    20971519     9972736   8e  Linux LVM
```

Multiply the number under the Start column by 512 and you'll get the byte offset of the partition inside the file.  You can use that number to mount a non-LVM partition.

To mount the first partition on a directory called /mnt/p1 in the example above:
```
mount -o loop,offset=1048576 disk.img /mnt/p1
```

The second partition is a logical volume, so you can't directly mount it. Instead, map that partition to a loopback device. 
```
# losetup -f
/dev/loop1
# losetup /dev/loop1 disk.img -o525336576
```

Then you can apply the LVM procedures in the next section to get at the volumes.


## Mounting Logical Volumes

To mount LVM partitions, the volume group(s) first need to be activated.  There's some good info at David Hilley's blog, which Ive simplified a bit here.

First, scan the system for LVM block devices, also known as physical volumes.  You'll see the PV's of the running system as well as the new NBD volumes. 
```
# lvm pvscan
PV /dev/nbd0p2 VG VolGroup00 lvm2 [7.69 GiB / 0 free]
PV /dev/sda2 VG vg_scott-kvm lvm2 [135.47 GiB / 0 free]
PV /dev/sdb1 VG vg_scott-kvm lvm2 [951.78 GiB / 0 free]
```

For this example, VolGroup00 is the guy we want to get to.  A volume group is just that: a collection of logical volumes.  The first step in getting to the LV's inside is to activate the volume group.
```
vgchange -ay VolGroup00
```

Scan the system for logical volumes.  (Note that the lvm scan/list commands are picking up the LV devices on the host as well as the QEMU guest image.)
```
# lvm lvs
LV      VG            Attr    LSize [...]
LvLogs  VolGroup00   -wi-a--- 3.66g 
LvRoot  VolGroup00   -wi-a--- 3.59g 
LvSwap  VolGroup00   -wi-a--- 448.00m 
lv_home vg_scott-kvm -wi-ao-- 48.84g 
lv_root vg_scott-kvm -wi-ao-- 50.00g 
lv_swap vg_scott-kvm -wi-ao-- 49.09g
lv_var  vg_scott-kvm -wi-ao-- 939.31g
```

The new logical volumes are now available as mountable filesystem devices.  Take a look in /dev/mapper.  The names of the device files there should be in the format VG-LV, where VG is the volume group name and LV is the name of the logical volume. 
```
# mount /dev/mapper/VolGroup00-LvRoot /mnt/some-root
```

Once you are finished examining or modifying your logical volume, be sure to unmount it and deactivate:
```
# umount /mnt/some-root
# vgchange -an VolGroup00
# losetup -d /dev/loop1
```

So, it's pretty simple right?  There may be some nuances that I'm not aware of, so chime in if your experience is different.

Here's a hacky bash module that provides two functions: the first is for attaching the logical volume to the loop device, and the second is for mounting the root volume. It's hacky because I cheated with global vars and replaced the actual cleanup code in my module with a comment. Those things should be fixed before adding capabilities to this code.
```
#!/bin/bash
cleanup() {
    echo "Cleaning up..."
    # unmount, deactivate volume group, detach loop device
}
```

#### usage: setupRootPart /path/to/image
#### return: loop device via global var loopdev
```
setupRootPart() {
    declare -g loopdev
    imagefile=$1

    offset_blocks=$(fdisk -l $imagefile | grep 8e.*LVM | awk '{print $2}')
    let offset=$offset_blocks*512
    loopdev=$(losetup -f)
    echo "Attaching $imagefile to $loopdev at offset $offset"
    if ! losetup $loopdev $imagefile -o $offset; then
        echo "Failed to set up loop device"
        cleanup
        exit 2
    fi
}
```

#### usage: mountRootVol /path/to/mount/dir
#### return: volume name via global var vol 
```
mountRootVol() {
    declare -g vol  # global var to return volume name to the caller
    mountpoint=$1

    vol=$(lvm pvscan | grep $loopdev | awk '{print $4 }')
    vgchange -ay $vol
    [[ -d $mountpoint ]] || mkdir -p $mountpoint
    # TODO need smarter way to find voldev
    voldev=/dev/mapper/$vol-root
    [[ -L $voldev ]] || {
        echo "No $voldev"
        echo "Mapped vols:"
        ls -l /dev/mapper
        cleanup
        exit 3
    }
    echo "Mounting $voldev on $mountpoint"
    mount $voldev $mountpoint
}
```


# Build VM based on cloud image.

http://mojodna.net/2014/05/14/kvm-libvirt-and-ubuntu-14-04.html


meta-data
```
hostname:  dv2-lab-vfdc-openstack4-mgt
local-hostname:  dv2-lab-vfdc-openstack4-mgt
instance-id:  dv2-lab-vfdc-openstack4-mgt
network-interfaces: |
  auto ens3
  iface ens3 inet static
  address 158.186.179.12
  netmask 255.255.255.192
  gateway 158.186.179.62
  dns-search ustest.lmco.com
  dns-nameservers 192.5.147.1 192.5.147.2 
```

new-vm.sh
```
#!/bin/bash

# sed -i 's/10.13.132.62/10.13.132.197/' user-data
# sed -i 's/10.13.132.62/10.13.132.197/' meta-data
# sed -i 's/appformix/i-contrail-analytics-vm/' user-data
# sed -i 's/appformix/i-contrail-analytics-vm/' meta-data
# sed -i 's/appformix/i-contrail-analytics-vm/' new-vm.sh

# update ssh_authorized_keys in user-data

# sed -i 's/eth0/ens3/' meta-data
# /etc/qemu-kvm/bridge.conf needs to have bridges to use (ex, br-ex)

set -x

VM_NAME=dv2-lab-vfdc-openstack4-mgt
VCPUS=12
RAMSIZE=48000
DISKSIZE=100G
BRIDGE1=br-620
BRIDGE2=br-810

virsh destroy $VM_NAME
virsh undefine $VM_NAME --remove-all-storage
#sudo rm -f $VM_NAME.qcow2

rm -f init.iso
genisoimage -o init.iso -volid cidata -joliet -rock user-data meta-data

#cp ../images/ubuntu-14.04-server-cloudimg-amd64-disk1.img $VM_NAME.qcow2
cp ../ubuntu-16.04-server-cloudimg-amd64-disk1.img $VM_NAME.qcow2
qemu-img resize $VM_NAME.qcow2 +$DISKSIZE

virt-install \
--virt-type kvm \
--name $VM_NAME  \
--vcpu $VCPUS \
--ram $RAMSIZE \
--disk $VM_NAME.qcow2,format=qcow2 \
--network bridge=$BRIDGE1 \
--network bridge=$BRIDGE2 \
--graphics vnc,listen=0.0.0.0 \
--noautoconsole \
--os-type=linux \
--os-variant=ubuntu16.04 \
--import \
--cpu host \
--disk path=init.iso,device=cdrom


virsh autostart $VM_NAME
```
 
user-data
```
#cloud-config
disable_root: false
manage_etc_hosts: true
chpasswd:
  list: |
    root:cubswin
    ubuntu:ubuntu
  expire: False
ssh_authorized_keys:
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDyyvzxdmtEpO7s5rhAfsCyH3A8aBfHGv4FelhHVHyOzqA2zsiGv/2Yhz+BurlfsIV7xcPGTdpuaj+x/Lyp44zJawP9/9TjKyOg9GZI0Ssr3KKEFYq4bovB1QM8OAv012f6DkvAuWZBMKBqOOzo0PARtoljsGnqTnGkpKPad+RIc76FEN+yQ0cYQ6n96tcwkihrUYVqZDSpUDVArH5vLuQZDpZOObOOPNPNYiFBCrG9cPQ4FrKiHH/1Qr4pXR1Jice41z+OR+XXjecIAWvesXPbFfDkKpGA56ikRvsgkI+MHcHRC9S3280Y2qeYB6IGT+73dFNUOGU1JTkQSqGNKbtd root@dv2-lab-vfdc-brazenbull-host.ustest.lmco.com
ssh_pwauth: True
final_message: "The system is finally up, after $UPTIME seconds"
fqdn:  dv2-lab-vfdc-openstack4-mgt.ustest.lmco.com
groups:
  - cloud-users
runcmd:
  - sed -i 's/PermitRootLogin .*/PermitRootLogin yes/g' /etc/ssh/sshd_config
  - service ssh restart
  - echo 158.186.179.10 dv2-lab-vfdc-contrail4-sm-mgt.ustest.lmco.com dv2-lab-vfdc-contrail4-sm-mgt >> /etc/hosts
  - echo 158.186.179.11 dv2-lab-vfdc-contrail4-mgt.ustest.lmco.com dv2-lab-vfdc-contrail4-mgt >> /etc/hosts
  - echo 158.186.179.12 dv2-lab-vfdc-openstack4-mgt.ustest.lmco.com dv2-lab-vfdc-openstack4-mgt >> /etc/hosts
  - echo 158.186.179.17 dv2-lab-vfdc-compute4-mgt.ustest.lmco.com dv2-lab-vfdc-compute4-mgt >> /etc/hosts
  - echo export http_proxy=http://proxy-lmi.global.lmco.com >> /etc/bash.bashrc
  - echo export http_proxys=http://proxy-lmi.global.lmco.com >> /etc/bash.bashrc
  - echo export HTTP_PROXY=http://proxy-lmi.global.lmco.com >> /etc/bash.bashrc
  - echo export HTTPS_PROXY=http://proxy-lmi.global.lmco.com >> /etc/bash.bashrc
  - echo export ALL_PROXY=http://proxy-lmi.global.lmco.com >> /etc/bash.bashrc
  - echo export NO_PROXY=127.0.0.1,158.186.179.10,158.186.179.11,158.186.179.12,158.186.179.13,158.186.179.14,158.186.179.15,158.186.179.16,158.186.179.17,192.168.207.33,192.168.207.34,192.168.207.35,192.168.207.36 >> /etc/bash.bashrc
manage_etc_hosts: False
power_state:
  mode: reboot
  timeout: 120 
```

