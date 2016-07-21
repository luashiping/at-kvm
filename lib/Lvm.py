#!/usr/bin/python
#-*- coding: UTF-8 -*-
import lvm2py

class Lvm():
    def __init__(self):
        self.lvm = lvm2py.LVM()
    
    def _get_vg(self,VgName,mode):
        vg = self.lvm.get_vg(VgName, mode)
        return vg
        
    def _create_lv(self,VgName,mode,LvName,DiskSize):
        vg = self._get_vg(VgName,mode)
        lv = vg.create_lv(LvName,DiskSize,"GiB")
        return lv
        