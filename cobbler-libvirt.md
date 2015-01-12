#Build virtual machine automatically with libvirt and Cobbler
This is based on the server with CentOS 7 minimum installation.

##Install Packages
* Install wget.
```
# yum install wget
```
* Add EPEL repository.
```
# wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
# rpm -ivh epel-release-7-2.noarch.rpm
```
* Install KVM and libvirt.
* Install Cobbler and required packages.
```
# yum install cobbler syslinux httpd pykickstart
# systemctl enable httpd
# systemctl start httpd
# systemctl enable cobblerd
# systemctl start cobblerd
```

##Configure Cobbler
* Generate encrypted password.
```
# openssl passwd -1
```
* Configure the following options in `/etc/cobbler/settings`.
```
default_password_crypted: "<encrypted password>"
manage_dhcp: 1
manage_dns: 1
manage_tftp: 1
restart_dhcp: 1
restart_dns: 1
pxe_just_once: 1
next_server: <Cobbler server IP address>
server: <Cobbler server IP address>
```
* Configure the following options in `/etc/cobbler/modules.conf`.
```
[dns]
module = manage_dnsmasq

[dhcp]
module = manage_dnsmasq

[tftpd]
module = manage_in_tftpd
```
* Configure the following options in `/etc/cobbler/dnsmasq.template`.
```
# There is already an instance of dnsmasq running for libvirt and listening to
# libvirt virtual bridge, so bind-interfaces is requred for this instance.
interface=<interface on which the server listens to DHCP requests>
bind-interfaces

dhcp-range=<start IP address>,<end IP address>

# Cobbler uses $next_server as the DHCP option routers (gateway).
# In this case, the real gateway is configured instead.
#dhcp-option=3,$next_server
dhcp-option=option:router,<gateway IP address>
```
* Synchronize and check Cobbler configurations.
```
# systemctl restart cobblerd
# cobbler sync
# systemctl enable xinetd
# systemctl start xinetd
# cobbler check
```

##Configure System
* Import distro.
```
# mkdir -p /mnt/iso
# mount -o loop <CentOS 7 Minimum ISO file> /mnt/iso
# cobbler import --arch x86_64 --path /mnt/iso --name centos7-min
# umount /mnt/iso
# cobbler distro report --name centos7-min
# cobbler profile report --name centos7-min-x86_64
```
* Specify kickstart file for the profile.
```
# cobbler profile edit --name centos7-min-x86_64 --kickstart /var/lib/cobbler/kickstarts/centos7.ks
```
* Add and configure a system.
```
# cobbler system add --name vm131 --profile centos7-min-x86_64
# cobbler system edit --name vm131 --hostname vm131 --interface eth0 --ip-address 10.161.208.132 --mac 52:54:00:76:a5:2b
```
* Apply all changes.
```
# cobbler sync
```

##Configure VM
* Pre-allocate disk image for each VM.
```
# qemu-img create -f raw vm131 20G
```
* Generate VM XML file. MAC address is pre-assigned for each VM in template.sh.
```
# template.sh vm131 1 16
```

##Launch VM
```
# virsh create vm131.xml
```
Use VNC client connecting to the server to watch the installation.


