#!/usr/bin/python
#-*- coding: UTF-8 -*-
#from __future__ import division
import os
import sys
import threading

mycwd = os.getcwd()
libcwd = mycwd+'/lib'
sys.path.append(libcwd)

from option import *
import VirtConnection
from Vm import * 

uri_list = ['qemu:///system']

##宿主机可用资源
def rc(uri):
    conn = VirtConnection.VirtConnection(uri)
    activedomains = conn.list_activedomains()

    node_vcpus = conn.get_node_vcpus()
    vcpus_total = 0
    for domain in activedomains:
        vcpus_total += conn.get_dom_current_vcpus(domain)
    ptgreen_no_enter("已用vcpu:")
    print vcpus_total
    ptgreen_no_enter("可用vcpu:")
    print node_vcpus - vcpus_total - 1 

    node_memory = conn.get_node_memory()
    memory_total = 0
    for domain in activedomains:
        memory_total += conn.get_dom_memory(domain)
    ptgreen_no_enter("已用内存:")
    print memory_total / 1024.0,"G"
    ptgreen_no_enter("可用内存:")
    print (node_memory - memory_total) / 1024.0,"G"
    
    vm_name = optdict['vm_name']
    alldomains = conn.list_alldomians()
    if vm_name in alldomains:
        ptred("The domain is exists")
        sys.exit()
    return conn

for i in uri_list:
    conn = rc(i)

condition = raw_input('Whether or not to continue["yes" or "no"]?')
if condition == 'yes':
    pass
else:
    sys.exit()

##########################################
##########生成xml文件,并创建磁盘######
##########################################
guest = Vm(optdict)
guest._set_disk_create_xml()
xmlfile = guest._get_xml_file()
f1 = open(xmlfile,"r+")
xml_content = f1.read()
clock_replace = ['<clock offset="utc"/>',"<cpu mode='host-passthrough'/>\n  "+'<clock offset="localtime"/>']
xml_content = xml_content.replace(clock_replace[0],clock_replace[1])
f1.seek(0)
f1.write(xml_content)
f1.close()

####修改镜像IP,主机名,密码
guest._modify_mirror()


######启动虚拟机
dom = conn.define_xml(xmlfile)
if dom:
    dom.create()
