#!/usr/bin/python
#-*- coding: UTF-8 -*-
from getopt import *
import sys
from FontColor import *

def usage():
      print """
Options: 
  -t template      Name of the template image
  -n name          Name of the guest instance
  --vcpus=VCPUS    Number of vcpus to configure for your guest.Ex:
                   --vcpus=5
  -r MEMORY        Memory to allocate for guest instance in megabytes
  --ip=IP          ip address of the guest instance
  --format=FORMAT  the image fomat of root disk 
  --disk=digital   Size of data disk (units are GiB)
  
            """
      exit()  
            
args = sys.argv[1:]
optdict = {}

try:
    optlist, args = getopt(args, 't:n:r:h',[  'vcpus=',  
                                              'ip=',
                                              'format=',
                                              'disk=',
                                              'help'
                                              ]
                              )
except GetoptError,e:
    print e
    sys.exit()

if not optlist or args:
    usage()

if len(optlist) < 6 or len(optlist) > 7:
    usage()

for option,value in optlist:
    if option in ["-h","--help"]: 
        usage()
    elif option == "-t":
        optdict['mirror_name'] = value
    elif option == "-n":
        optdict['vm_name'] = value
    elif option == "--vcpus":
        optdict['vcpus'] = value
    elif option == "-r":
        optdict['mem'] = value
    elif option == "--ip":
        optdict['ip'] = value
    elif option == "--format":
        optdict['root_disk_format'] = value
    elif option == "--disk":
        if value.isdigit():
            optdict['data_disk_size'] = value
        else:
           ptred("--disk parameters must be numeric")
           sys.exit()