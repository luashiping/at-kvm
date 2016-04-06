#!/usr/bin/python
#-*- coding: UTF-8 -*-
a = ''
b = 'False'

def test():
	return 'babab'

def ddd():
	return "cccc"

a = b if b else test()
print a