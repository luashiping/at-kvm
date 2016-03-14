#!/usr/bin/python
#-*- coding: UTF-8 -*-
import random
import string
import socket
import subprocess
from FontColor import *
from passlib.hash import sha512_crypt

##随机密码
def rand_password(bit):
    password = string.join(random.sample(string.digits+string.letters, bit)).replace(' ','')
    return password

##sha512_crypt 密码哈希
def sha512_encrpt(password):
    sha512_password = sha512_crypt.encrypt(str(password))
    return sha512_password

##获取主机名
def get_hostname():
	return socket.gethostname()

##根据主机名获取主机ip
def get_hostadrr():
	myname = get_hostname()
	return socket.gethostbyname(myname)

##ip检测
def check_ip(ip):
	try:
		res = subprocess.call(['ping', '-c', '1', ip])
		if res == 0:	
			ptred("危险提示:你所设定的虚拟机IP地址可能与现有IP地址产生冲突,请更换")
			exit(1)
	except OSError:
		print ('check ip does not work')