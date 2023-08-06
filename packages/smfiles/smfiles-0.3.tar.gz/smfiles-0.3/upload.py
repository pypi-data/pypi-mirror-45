from setuptools import setup

setup(
name='smfiles', 
version='0.3',
author='张乐涛', 
author_email='1668151593@qq.com', 
url='https://github.com/zhangletao/smfiles', 
description='Read and Edit .sm files.',
long_description='''
# How to use this package


from smfiles import read, edit, version, datetime


print(read.StepMania('xxx.sm').bpms)


>>> 0.000=156.000, 8.000=312.000


edit.StepMania('yyy.sm').SetTitle('mytitle')


print(version, datetime)


>>> 0.2 2019-05-04
''',
packages=['smfiles'], 
install_requires=[])