#!/usr/bin/env python
# -*- coding: utf-8 -*
# @Date    : 2019-04-12 09:56:01
# @Author  : Blackstone
# @to      :

# coding=utf-8
import re
import time
import logging
import os
import cx_Oracle
from ._gen import Gen
from . import Rule
class DBHelper:

    _connect_pool={}

    def __init__(self,config_path=None):

        self.config=Gen.get_config(config_path)

        if self.config is None:

            self.config=self.get_config_template()

            Gen.log("--------------")
            Gen.log("正通过模板方法['get_config_template']连接库.")
            Gen.log("--------------")
            Gen.log("默认模板数据为=> ",self.config)

        if not isinstance(self.config,dict):
            raise TypeError("config是字典=>",self.config)


  

    def _db_connect(self):


        Gen.log("----------------------")
        Gen.log("----尝试连接数据库-----")
        Gen.log("----------------------")

        try:



            self.dbtype=self.config["dbtype"]
            self.dbname=self.config["dbname"]
            #oracle不需要这两项
            self.host=self.config["host"]
            self.port=self.config["port"]
            self.user=self.config["username"]
            self.pwd=self.config["password"]

            key="+".join([self.dbtype,self.dbname,str(self.host),str(self.port),self.user,str(self.pwd)])

            Gen.log("数据库类型=>",self.dbtype)

            Gen.log("数据库名=>",self.dbname)
            Gen.log("数据库地址(仅mysql|db2)=>",self.host,self.port)
            Gen.log("数据库账号=>",self.user,self.pwd)

            self.conn=self._connect_pool.get(key)

            if  self.conn is not None:
                pass

            else:
                if self.dbtype.lower()=='mysql':
                    import pymysql
                  
                    self.conn = pymysql.connect(db=self.dbname, host=self.host,
                                                port=int(self.port),
                                                user=self.user,
                                                password=str(self.pwd),
                                                charset='utf8mb4')

                elif self.dbtype.lower()=='oracle':
                    self.conn =cx_Oracle.connect(self.user+'/'+self.pwd+'@'+self.dbname)

                elif self.dbtype.lower()=='db2':
                    import ibm_db_dbi
                    self.conn = ibm_db_dbi.connect("PORT="+str(self.port)+";PROTOCOL=TCPIP;", 
                                                   user=self.user,
                                                   password=self.pwd, 
                                                   host=self.host, 
                                                   database=self.dbname)

                self._connect_pool[key]=self.conn


            Gen.log("连接成功,获得=>%s"%self.conn)
           


        except cx_Oracle.DatabaseError:
            raise RuntimeError("配置不正确")

    def _db_commit(self):
        try:
            if self.conn:
                self.conn.commit()
        except:
            pass


    def db_close():
        try:
            [con.close() for con in DBHelper._connect_pool.values()]
         
        except  Exception as ee:
            Gen.log(ee)

            raise DBError('关闭数据库连接出现异常，请确认')

                
    def db_execute(self, sql,error="ignore-"):

        res=0

        Gen.log("执行sql=>",sql)

        self._db_connect()
        cursor=self.conn.cursor()

        try:
            res=cursor.execute(sql)

            if not sql.split()[0].lower().startswith("select"):
                self.conn.commit()

            if sql.split()[0].lower().startswith("select"):
                res=cursor.fetchall()

        except Exception as e:
            if error=='ignore':
                return res

            Gen.log("出现异常=>"+str(e))
            raise RuntimeError("sql执行结果报错.")
        finally:

            cursor.close()
            if isinstance(res,int):
                Gen.log("执行结果=>%s(生效行数)"%(res,))
            else:
                Gen.log("执行结果=>%s"%(res,))  
            Gen.log("\n\n")

            return res
        #return sqlresult

  
    def get_config_template(self):
        return {

        'dbtyee':'mysql',
        'dbname':'auto',
        'host':'127.0.0.1',
        'port':3306,
        'user':'root',
        'password':123456


        }



        

    @classmethod
    def get_dao_gen_rule(cls):
        pass


 
class DBError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


if __name__=="__main__":
    
    data={
    'dbtype':'mysql',
    'dbname':'auto',
    'host':'127.0.0.1',
    'port':'3306',
    'password':"123456",
    'username':'root',
    'password':'123456'

    }


    h=DBHelper(data)
    res=h.db_execute("select * from device")


