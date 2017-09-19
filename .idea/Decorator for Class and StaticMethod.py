#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 给类和静态方法提供装饰器

# 确保装饰器在@classmethod和@staticmethod

import time
from functools import wraps

# a simple decorator
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return r
    return wrapper

# class illustrate application of the decorator to different kinds of methods
class Spam:
    @timethis
    def instance_method(self, n):
        print(self, n)
        while n > 0:
            n -= 1

    @classmethod
    @timethis
    def class_method(cls, n):
        print(cls, n)
        while n > 0:
            n -= 1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n > 0:
            n -= 1


# 问题: 想在装饰器中给包装函数增加额外的参数, 但是不影响现有函数的调用规则

from functools import wraps

def optional_debug(func):
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling ', func.__name__)

        return func(*args, **kwargs)
    return wrapper


# 问题: 通过反省或者重写地拿以的某些部分来修改它的行为, 但是不继承或者元类的方法

# 类装饰器, 下面是重写特殊方法__getattribute__的类装饰器

def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__

    # make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls

# Example use
@log_getattribute
class A:
    def __init__(self, x):
        self.x = x

    def Spam(self):
        pass


# 类装饰器通常可以作为高级技术混入和元类的一种简洁的代替方案
