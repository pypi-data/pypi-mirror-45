
# from dbhelper import *
# from decorator import *
# from _gen import *
import os
root_path=os.path.dirname(os.path.dirname(__file__))
config_path=os.sep.join([root_path,"config"])
test_path=os.sep.join([root_path,"test"])


#
from collections import namedtuple
Rule =namedtuple("Rule",['tablename','support','keys'])

def upcasefirst(str_):
	return str_[0].upper()+str_[1:]


def lowcasefirst(str_):
	return str_[0].lower()+str_[1:]