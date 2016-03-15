#!/usr/bin/python
#-*- coding: UTF-8 -*-
import os
import shutil
from Lvm import *
import Gfs
from pub_function import *
from Config import *

class Vm:
    def __init__(self,optdict={}):
        self._xml_dir = "./vm_xml/"
        self._host = get_hostadrr()
        self._vg_name = "vg_"+ get_hostname()
        self._config_info = Config('vm.cfg')
        self._vm_pool = self._config_info.get('defaults','vm_pool')
        self._mirror_pool = self._config_info.get('defaults','mirror_pool')
        self._internal_br = self._config_info.get('defaults','internal-net')
        self._external_br = self._config_info.get('defaults','external-net')
        self._script_dir = "./script/"
        self._vm_name = optdict['vm_name']
        self._memory = optdict['mem']
        self._vcpus = optdict['vcpus']
        self._root_disk_fromat = optdict['root_disk_format']
        self._data_disk_path = None
        self._mirror_name = optdict['mirror_name']
        self._ip = optdict['ip']
        check_ip(self._ip)
        self._hostname = self._vm_name
        self._is_exist = None
        if optdict.has_key('data_disk_size'):
            self._data_disk_size = int(optdict['data_disk_size'])
            self._is_exist = True
    
    def _get_xml_file(self):
        xml_file = self._xml_dir + self._vm_name+".xml"
        create_xml = "virt-install \\"
        
        add = lambda x: self.xml_append(create_xml, x)
        
        create_xml = add("--name %s \\" % self._vm_name)
        create_xml = add("--vcpus %s \\" % self._vcpus)
        create_xml = add("--ram %s \\" % self._memory)
        create_xml = add(self._get_disk_create_xml())
        create_xml = add("--network bridge="+self._internal_br+" \\") if self._internal_br else add("--network bridge=br0 \\")
        create_xml = add("--network bridge="+self._external_br+" \\") if self._external_br else add('')
        create_xml = add("--graphics vnc,listen="+self._host+" \\")
        create_xml = add("--noautoconsole \\")
        create_xml = add("--os-type=linux \\")
        create_xml = add("--os-variant=rhel6 \\")
        create_xml = add("--import \\")
        create_xml = add("--print-xml > %s" % xml_file)
        createxml_temp = os.system(create_xml)
        if not createxml_temp:
            return xml_file
        else:
            return False
        

    def _set_disk_create_xml(self):
        disk_xml_format = "--disk path=%s,bus=virtio,cache=writethrough,format=%s,io=native \\"
        
        self._root_disk_path = self._get_root_disk_path()
        self._data_disk_path = self._get_data_disk_path(self._is_exist)
        self._disk_xml = disk_xml_format % (self._root_disk_path,self._root_disk_fromat)
        if self._data_disk_path:
            self._disk_xml += "\n" + disk_xml_format % (self._data_disk_path,"raw")
                
    def _get_disk_create_xml(self):
        return self._disk_xml
    
    
    def _get_root_disk_path(self):
        if self._root_disk_fromat == 'raw':
            root_disk_path = "/dev/"+self._vg_name+"/"+self._vm_name
        elif self._root_disk_fromat == 'qcow2':
            root_disk_path = self._vm_pool+self._vm_name+".qcow2"
            
        ret = self._create_root_disk(root_disk_path)
        if ret:
            return root_disk_path
        else:
            return False
       
       
    def _get_data_disk_path(self,is_exist=False):
        if is_exist:
            data_disk_path = "/dev/"+self._vg_name+"/"+self._vm_name+"-data"
            ret = self._create_data_disk(data_disk_path)
            if ret:
                return data_disk_path
            else:
                return False
        return False
            
    def _create_root_disk(self,path):
        if self._root_disk_fromat == 'qcow2':
            shutil.copy(self._mirror_pool+self._mirror_name,path)
            return True
        else:
            return False
            
    def _create_data_disk(self,path):
        if self._is_exist:
            lvm = Lvm()
            lv_result = lvm._create_lv(self._vg_name,"w",self._vm_name+"-data", self._data_disk_size)
            #g = Gfs.Gfs(path,readonly=0)
            #g._mkfs("ext4","/dev/sda")
            return True
        else:
            return False
            
    def _modify_mirror(self):
        self.g = Gfs.Gfs(self._root_disk_path,readonly=0)
        root_partion = self.g._inspect_os()
        for i in root_partion:
            self.g._mount(i,"/")
        self._injection_ssh_key()
        self._modify_root_password()
        self._modify_network()
        self._modify_hostname()
        self._mount_data_disk()
            
    def _injection_ssh_key(self):
        fk = open(self._script_dir+"/pubkey.sh",'r')
        key_info = fk.read()
        self.g._sh(key_info)
        
    def _modify_root_password(self):
        password = rand_password(14)
        print password
        sha512_password = sha512_encrpt(password)
        shadow_file = "/etc/shadow"
        #g.sh("sed -ir '/^root/s#root:([^:]+):(.*)#root:'"+sha512_password+"':\2#' /etc/shadow")#没报错但是修改 不成功
        shadow_data = self.g._read_file(shadow_file)
        s_file = shadow_data.split("\n")
        new_s_file = []                                                             
        for entry in s_file:                                                        
            split_entry = entry.split(":")                                          
            if split_entry[0] == "root":                                            
                split_entry[1] = sha512_password                     
                                                                                
            new_s_file.append(':'.join(split_entry))                                
                                                                                
        new_shadow_data = '\n'.join(new_s_file)
        self.g._write(shadow_file,new_shadow_data)

    def _modify_network(self):
        iface_filename = "/etc/sysconfig/network-scripts/ifcfg-eth0"
        nic_info = "DEVICE=eth0\nTYPE=Ethernet\nONBOOT=yes\nNM_CONTROLLED=yes\nBOOTPROTO=static\nIPADDR="+self._ip+"\nNETMASK=255.255.255.0"
        self.g._write(iface_filename,nic_info)
        
    def _modify_hostname(self):
        hostname_filename = "/etc/sysconfig/network" 
        hostname_info = "NETWORKING=yes"+"\n"+"HOSTNAME="+self._hostname
        self.g._write(hostname_filename,hostname_info)
        
    def _mount_data_disk(self):
        if self._is_exist:
            boot_content = "mount /dev/vdb /data"
            self.g._write_append("/etc/rc.local",boot_content)

    def _check_ip(self):
        pass
        
    def xml_append(self,orig,new):
        """
        Little function that helps generate consistent xml
        """
        if not new:
            return orig
        if orig:
            orig += "\n"
        return orig + new
