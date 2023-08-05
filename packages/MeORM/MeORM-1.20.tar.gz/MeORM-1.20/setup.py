from distutils.core import setup
from setuptools import find_packages
#导入setup函数
 
setup(
	  name="MeORM", 
	  version="1.20",
	  description="orm框架",
	  author="blackstone",
	  author_email="971406187@qq.com",
	  url="https://github.com/Blackstone1204",
	  #py_modules=['morm']
	  packages=find_packages(),
# 	  package_data = {
# 	  # If any package contains *.txt or *.rst files, include them:
# 	  '': ['*.txt', '*.rst'],
# 	  # include any *.msg files found in the 'hello' package, too:
# 	  'hello': ['*.msg'],
# }

	  data_files=[("config",["connect","dao_gen"])]
	  )