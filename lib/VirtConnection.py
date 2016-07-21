#!/usr/bin/python
#-*- coding: UTF-8 -*-
import libvirt
from xml.etree import ElementTree

class VirtConnection():
    def __init__(self,uri):
        self.conn = libvirt.open(uri)
    
    def list_alldomians(self):
        alldomains = []
        listAllDomains = self.conn.listAllDomains(0)
        for i in listAllDomains:
            alldomains.append(i.name())
        return alldomains
        '''
        alldomains = self.conn.listDefinedDomains()
        for id in self.conn.listDomainsID():
            dom = self.conn.lookupByID(id)
            alldomains.append(dom.name())
            #infos = dom.info()
            print 'Name =  %s' % dom.name()
            print 'ID = %d' % id
            print 'State = %d' % infos[0]
            print 'Max Memory = %d' % infos[1]
            print 'Number of virt CPUs = %d' % infos[3]
            print 'CPU Time (in ns) = %d' % infos[2]
            print ' '
        '''
        
    def list_activedomains(self):
        activedomains = []
        listActiveDomains = self.conn.listAllDomains(1)
        for i in listActiveDomains:
            activedomains.append(i.name())
        return activedomains
        
    def define_xml(self,DomianXmlFile):
        f = open(DomianXmlFile)
        xml_content = f.read()
        try:
            dom = self.conn.defineXML(xml_content)
            return dom
        except Exception:
            #print "%s" % e
            return 0
            
    def list_blocks(self,DomainName):
        dom = self.conn.lookupByName(DomainName)
        tree = ElementTree.fromstring(dom.XMLDesc(0))
        devices = []
        for target in tree.findall("devices/disk/target"):
            dev = target.get("dev")
            devices.append(dev)
        return devices
         
    def get_dom_memory(self,DomainName):
        dom = self.conn.lookupByName(DomainName)
        memorylist = dom.memoryStats()
        memory = memorylist['actual'] / 1024
        return memory
        
    def get_node_memory(self):
        sysinfo = self.conn.getSysinfo(0)
        tree = ElementTree.fromstring(sysinfo)
        memory = 0
        for target in tree.findall("memory_device/entry"):
            if target.get("name") == "size":
                memory += int(target.text.rstrip('MB'))
        return memory
        
    def get_dom_current_vcpus(self,DomainName):
       dom = self.conn.lookupByName(DomainName)
       return dom.vcpusFlags(libvirt.VIR_DOMAIN_AFFECT_CURRENT)
       
    def get_dom_max_vcpus(self):
        dom = self.conn.lookupByName(DomainName)
        return dom.maxVcpus()
        
    def get_node_vcpus(self):
        return self.conn.getMaxVcpus(None)
