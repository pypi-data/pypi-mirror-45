﻿from setuptools import setup

setup(
name='smfiles', 
version='0.0.1', 
author='张乐涛', 
author_email='1668151593@qq.com', 
url='https://github.com/zhangletao/smfiles', 
description='读取.sm文件', 
packages=['smfiles'], 
install_requires=[], 
entry_point={'console_scripts':['StepMania=smfiles:StepMania']})