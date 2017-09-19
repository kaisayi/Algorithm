#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 有一个函数或者方法, 它使用*args和**kwargs作为参数, 这样比较通用, 但有时想检查
# 传递进来的参数是不是某个想要的类型

# 方案: 对任何涉及到操作函数调用签名的问题, 可以使用inspect模块中的签名特性.

from inspect import Signature, Parameter
# make a signature for a func(x, y=43, *, z=None)
parms = [Parameter('x', Parameter.POSITIONAL_OR_KEYWORD),
         Parameter('y', Parameter.POSITIONAL_OR_KEYWORD, default=43),
         Parameter('z', Parameter.KEYWORD_ONLY, default=None)]

sig = Signature(parms) # sig = (x, y=43, *, z=None) 签名对象

# 一旦有了签名对象, 就可以使用它的bind方法将它绑定到*args和**kwargs

def func(*args, **kwargs):
    bound_values = sig.bind(*args, **kwargs)
    for name, value in bound_values.arguments.items():
        print(name, value)


# 下面是一个强制函数签名的具体例子

def make_sig(*names):
    parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
             for name in names]
    return Signature(parms)

class Structure:
    __signature__ = make_sig()
    def __init__(self, *args, **kwargs):
        bound_value = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_value.arguments.items():
            setattr(self, name, value)
# Example

class Stock(Structure):
    __signature__ = make_sig('name', 'shares', 'price')

class Point(Structure):
    __signature__ = make_sig('x', 'y')


# 还可以通过自定义元类来创建签名对象

class StructureMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsdict['__signature__'] = make_sig(*clsdict.get('_fields', []))
        return super.__new__(cls, clsname, bases, clsdict)

class Structure2(metaclass=StructureMeta):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound_value = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_value.arguments.items():
            setattr(self, name, value)

class Stock2(Structure2):
    _fields = ['name', 'shares', 'prices']

