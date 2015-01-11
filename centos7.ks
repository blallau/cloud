install
text
url --url $tree
lang en_US.UTF-8
keyboard us
timezone America/New_York
auth --enableshadow --enablemd5
rootpw --iscrypted $default_password_crypted
autopart
zerombr
bootloader --location=mbr --append="console=tty0 console=ttyS0,9600n8"
clearpart --all --initlabel

selinux --disabled
firewall --disabled
skipx

$SNIPPET('network_config')
reboot

%pre
#$SNIPPET('log_ks_pre')
$SNIPPET('kickstart_start')
$SNIPPET('pre_install_network_config')
%end

%packages
%end

%post
#$SNIPPET('log_ks_post')
$SNIPPET('post_install_kernel_options')
$SNIPPET('post_install_network_config')

yum install -y wget ntp
ntpdate 172.28.16.17
systemctl enable ntpd
systemctl start ntpd

$SNIPPET('kickstart_done')
%end

