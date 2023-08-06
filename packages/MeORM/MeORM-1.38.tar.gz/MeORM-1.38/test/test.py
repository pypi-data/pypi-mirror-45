#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-15 09:01:29
# @Author  : Blackstone
# @to      :



from morm import DBHelper




# class Device(object):

# 	@bind_sql("select * from device where serial={0}")
# 	def query_device(serial):
# 		pass
# 	@bind_sql("select * from device")
# 	def query_all_device():
# 		pass
# 	@bind_sql("update device set port={1} where serial={0}")
# 	def update_device(serial,port):
# 		pass

# 	@bind_sql("insert into device(serial,port) values({0},{1})")
# 	def add_device(serial,port):
# 		pass

# 	@bind_sql("delete from device where port={0}")
# 	def del_device(port):
# 		pass

# 	@insert
# 	def  add(deivce):
# 		pass

# 	@update(keys=("serial",))
# 	def update(device):
# 		pass

# 	@delete(keys=("serial",))
# 	def delete(device):
# 		pass


# 	@select(keys=("serial",))
# 	def query(device):
# 		pass



if __name__=="__main__":

	DBHelper()


