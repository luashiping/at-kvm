#!/usr/bin/python
#-*- coding: UTF-8 -*-
import guestfs

class Gfs():
    def __init__(self,path,readonly=0):
        self.g = guestfs.GuestFS(python_return_dict=True)
        self._path = path
        self.g.add_drive_opts(self._path,readonly=0)
        self.g.launch()
    
    def _mkfs(self,fstype,device):
        self.g.mkfs(fstype,device)
        
    def _mount(self,partion,mountpoints):
        self.g.mount(partion, mountpoints)
        
    def _inspect_os(self):
        root = self.g.inspect_os()
        return root
        
    def _sh(self,scrpit):
        self.g.sh(scrpit)
        
    def _read_file(self,path):
        content = self.g.read_file(path)
        return content
        
    def _write(self,path,content):
        self.g.write(path,content)
        
    def _write_append(self,path,content):
        self.g.write_append(path,content)
    
    def __del__(self):
        self.g.close()