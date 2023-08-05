#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-04-12 14:21:49
# @Author  : Blackstone
# @to      :

# def bind_sql(cls,func):
# 	def wrap(*args,**kw):
# 		Gen.log("func=>",func)
# 		Gen.log(args)
# 		Gen.log(kw)
# 		return func(*args,**kw)

# 	return wrap
	

from dbhelper
from ._gen import Gen
import re,datetime,warnings
from functools import update_wrapper
from . import lowcasefirst


class bind_sql(object):
	def __init__(self,sql,*args,**kw):
		self.sql=sql

		#print("self.ql=> ",self.sql)


	def __call__(self,func):
	
		#Gen.log("执行方法=>",func.__name__)

		def wrap(*args,**kw):

			Gen.log("执行方法=>%s.%s(%s,%s)"%(func.__module__,func.__name__,args,kw))


			if not hasattr(func,"_cache"):

				func._cache=self.sql

			else:
				self.sql=func._cache


			params=self.get_params(self.sql)

			#print(args,"=>",params)
			L1=len(params)
			L2=len(args)

			if not L1==L2:
				raise TypeError("sql[%s]和%s[%s]中参数个数不一致."%(L1,func.__name__,L2))

			for index in range(len(args)):
				v1='{%s}'%(index,)
				v2=None

				c=(int,float,bool,str)
				if isinstance(args[index],c):
					v2="'%s'"%str(args[index])

				else:
					raise TypeError("bind_sql修饰方法 参数类型只能为",c)
				#object case
				
				#print(v1,"=>",v2)
				self.sql=self.sql.replace(v1,v2)


			h=DBHelper()
			res=h.db_execute(self.sql)
			return res

		return wrap
		

	def get_params(self,sql):
		a= re.findall(r"{\d+}",sql)
		#print("fjajfpasjfdof**********************************")
		#print(sorted(a))
		return a





def insert(func):
	
	def wrap(*args,**kw):

		invoker =args[0]

		tablename=lowcasefirst(invoker.__class__.__name__)

		props=Gen.get_tabel_column_map().get(tablename)

		invoker.__class__.props=props

		values=[]

		used=[]
		for p in invoker.props:
			v=""
			if hasattr(invoker, p):
				used.append(p)
				v=eval("invoker.%s"%p)

				if isinstance(v, (str,datetime.datetime)):
					v="'%s'"%v

				# print(v)

				values.append(str(v))

		valuestr=",".join(values)

		colstr=",".join(used)

		sql="insert into %s(%s) values(%s)"%(tablename,colstr,valuestr)
		Gen.log("@insert sql=>",sql)

		h=DBHelper()
		res=h.db_execute(sql)
		return res
	return wrap


class update():
	def __init__(self,keys,*args,**kw):
		self.keys=keys

	def __call__(self,func):

		def wrap(invoker,*args,**kw):

			tablename=lowcasefirst(invoker.__class__.__name__)
	
			Gen.log("执行方法%s(%s,%s)@update 关键列%s"%(func.__name__,args,kw,self.keys,))

			if len(self.keys)==0:
				raise AttributeError("配置错误 @update使用表名keys必填.")

			props=Gen.get_tabel_column_map().get(tablename)
			#print("props=>",props)

			invoker.__class__.props=props

			not_keys=[p for p in props if hasattr(invoker,p) and p not in self.keys]

			#print("not keys=>",not_keys)

			x,y=[],[]
			for key in self.keys:
				if not hasattr(invoker,key):
					raise AttributeError("key列[%s]没设值"%key)
				x.append("%s='%s'"%(key,eval("invoker.%s"%key)))

			keystr=" and ".join(x)


			for key in not_keys:
				y.append("%s='%s'"%(key,eval("invoker.%s"%key)))

			notkeystr=" and ".join(y)
			sql="update %s set %s where %s"%(tablename,notkeystr,keystr)


			Gen.log("@update sql=>",sql)

			h=DBHelper()
			return h.db_execute(sql)

		return wrap



class delete():
	def __init__(self,keys,*args,**kw):
		self.keys=keys

	def __call__(self,func):

		def wrap(invoker,*args,**kw):

			tablename=lowcasefirst(invoker.__class__.__name__)
	
			Gen.log("执行方法%s(%s,%s)@delete 关键列%s"%(func.__name__,args,kw,self.keys,))

			if len(self.keys)==0:
				raise AttributeError("配置错误 @delete使用表名keys必填.")

			props=Gen.get_tabel_column_map().get(tablename)
			#print("props=>",props)

			invoker.__class__.props=props

			x=[]
			for key in self.keys:
				if not hasattr(invoker,key):
					raise AttributeError("key列[%s]没设值"%key)
				x.append("%s='%s'"%(key,eval("invoker.%s"%key)))

			keystr=" and ".join(x)

			sql="delete from  %s where %s"%(tablename,keystr)

			Gen.log("@delete sql=>",sql)

			h=DBHelper()
			return h.db_execute(sql)

		return wrap


class select():
	def __init__(self,keys,*args,**kw):
		self.keys=keys

	def __call__(self,func):

		def wrap(invoker,*args,**kw):

			tablename=lowcasefirst(invoker.__class__.__name__)
	
			Gen.log("执行方法%s(%s,%s)@select 关键列%s"%(func.__name__,args,kw,self.keys,))

			if len(self.keys)==0:
				raise AttributeError("配置错误 @select使用表名keys必填.")

			props=Gen.get_tabel_column_map().get(tablename)
			#print("props=>",props)

			invoker.__class__.props=props

			x=[]
			for key in self.keys:
				if not hasattr(invoker,key):
					raise AttributeError("key列[%s]没设值"%key)
				x.append("%s='%s'"%(key,eval("invoker.%s"%key)))

			keystr=" and ".join(x)

			sql="select * from  %s where %s"%(tablename,keystr)

			Gen.log("@select sql=>",sql)

			h=DBHelper()
			return h.db_execute(sql)

		return wrap



def get_connect_config():
	config=Gen.get_config()

	if config is None:
		config=DBHelper.get_config_template()

		Gen.log("--------------")
		Gen.log("正通过模板方法['get_config_template']连接库.")
		Gen.log("--------------")
		Gen.log("获得模板数据为=> ",config)


	return config
