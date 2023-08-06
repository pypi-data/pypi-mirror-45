# !usr\bin\env python
# -*- coding:utf-8 -*-

from .windows import *
from warnings import filterwarnings
filterwarnings('ignore')

version = '0.0.2'
author = '张乐涛'
datetime = '2019-05-02'


def load_smfile(file_name):
    return SMFile(file_name)

