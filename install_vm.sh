#!/bin/bash
##################################
#########虚拟机安装脚本###########
##################################
virt-install \
--virt-type=kvm \
--name=centos70 \
--vcpus=1 \
--ram=1024 \
--disk=/data/image/centos-70.qcow2,bus=virtio,cache=writethrough,format=qcow2,io=native \
--network bridge=br0 \
--graphics vnc,listen=0.0.0.0 \
--noautoconsole \
--os-type=linux \
--os-variant=rhel7 \
--cdrom "/data/iso/CentOS-7.0-1406-x86_64-Everything.iso"
#--import --print-xml

#--location http://192.168.1.22/centos6/ \
