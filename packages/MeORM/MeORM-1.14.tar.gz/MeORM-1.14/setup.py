from distutils.core import setup
from setuptools import find_packages
#导入setup函数
 
setup(
	  name="MeORM", 
	  version="1.14",
	  description="orm框架",
	  author="blackstone",
	  author_email="971406187@qq.com",
	  url="https://github.com/Blackstone1204",
	  #py_modules=['morm']
	  packages=find_packages()
	  )