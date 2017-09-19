#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 想要入一个模块, 但是模块的名字在字符串中, 想对字符串调用导入命令

# 方法: 使用importlib.import_module()函数来手动导入名字为字符串给出一个模块
# 或者包的一部分

import importlib
math = importlib.import_module('math')


# custmize python's import statement so that it can transparently load modules from a remote machine

#