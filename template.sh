#!/bin/sh

# template.sh <name> <cpu> <memory G>
# eg. template.sh vm131 1 16

name=$1
cpu=$2
let "memory = $3 * 1024 * 1024"
image=$name.img
mac_list="
    vm131=52:54:00:76:a5:2b
    vm132=52:54:00:52:19:86
    vm133=52:54:00:18:46:60
    vm134=52:54:00:84:b2:37
    vm135=52:54:00:36:97:e0
    vm136=52:54:00:91:28:72"

for i in $mac_list
do
  idx=`expr index $i =`
  if [ $name == ${i:0:idx-1} ]
  then
    mac=${i:idx}
  fi
done

cat << __EOT__ > $1.xml
<domain type='kvm'>
  <name>$name</name>
  <memory unit='KiB'>$memory</memory>
  <cpu mode='custom' match='exact'>
    <model fallback='allow'>Westmere</model>
    <vendor>Intel</vendor>
    <feature policy='require' name='vmx'/>
  </cpu>
  <currentMemory unit='KiB'>$memory</currentMemory>
  <vcpu placement='static'>$cpu</vcpu>
  <os>
    <type arch='x86_64'>hvm</type>
    <boot dev='network'/>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw' cache='none'/>
      <source file='/var/cloud/libvirt/images/$image'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='bridge'>
      <mac address='$mac'/>
      <source bridge='br-mgmt'/>
      <model type='virtio'/>
    </interface>
    <interface type='bridge'>
      <source bridge='br-data'/>
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
    <video>
      <model type='cirrus' vram='9216' heads='1'/>
    </video>
    <memballoon model='virtio'>
    </memballoon>
  </devices>
</domain>
__EOT__

