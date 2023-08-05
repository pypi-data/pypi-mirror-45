#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-15 09:01:29
# @Author  : Blackstone
# @to      :



# from morm import DBHelper,Gen,insert,delete,update,select,bind_sql


from setuptools import find_packages
print(find_packages())

class Device(object):

	@bind_sql("select * from device where serial={0}")
	def query_device(serial):
		pass
	@bind_sql("select * from device")
	def query_all_device():
		pass
	@bind_sql("update device set port={1} where serial={0}")
	def update_device(serial,port):
		pass

	@bind_sql("insert into device(serial,port) values({0},{1})")
	def add_device(serial,port):
		pass

	@bind_sql("delete from device where port={0}")
	def del_device(port):
		pass

	@insert
	def  add(deivce):
		pass

	@update(keys=("serial",))
	def update(device):
		pass

	@delete(keys=("serial",))
	def delete(device):
		pass


	@select(keys=("serial",))
	def query(device):
		pass



if __name__=="__main__":

	# DBHelper.get_config_template=lambda self:{
	# 'host':'fda'
	# }

	# Device.add_device("fdajlfdfafdafdsa",1112)
	# Device.add_device("fdajlfdfafda22",1112)


	d=Device()

	# d.touch_port=9999


	d.serial="fjdalsfdsaffffj"

	print(Device.query(d))



