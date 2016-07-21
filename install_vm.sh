#!/bin/bash
##################################
#########虚拟机安装脚本###########
##################################
virt-install \
--virt-type=kvm \
--name=test \
--vcpus=1 \
--ram=1024 \
--disk=/data/image/centos-6.6.qcow2_bak,bus=virtio,cache=writethrough,format=qcow2,io=native \
--network bridge=br1 --network bridge=br2 \
--graphics vnc,listen=192.168.18.21 \
--noautoconsole \
--os-type=linux \
--os-variant=rhel6 \
--import --print-xml

#--location http://192.168.18.22/centos6/ \
