#!/usr/bin/python
#-*- coding: UTF-8 -*-

def ptyellow(str):
    print  '\033[1;33m'+str+'\033[0m'
def ptred(str):
    print  '\033[1;31m'+str+'\033[0m'
def ptgreen(str):
    print  '\033[1;32m'+str+'\033[0m'
def ptyellow_no_enter(str):
    print  '\033[1;33m'+str+'\033[0m',
def ptred_no_enter(str):
    print  '\033[1;31m'+str+'\033[0m',
def ptgreen_no_enter(str):
    print  '\033[1;32m'+str+'\033[0m',
