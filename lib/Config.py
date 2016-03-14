#!/usr/bin/python
#-*- coding: UTF-8 -*-
import ConfigParser

class Config:
	def __init__(self, path):
		self.path = path
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(self.path)

	def get(self, field, key):
		result = ""
		try:
			result = self.cf.get(field, key)
		except:
			result = ""
		return result
