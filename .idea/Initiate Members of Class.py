#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 想在类被定义的时候就初始化一部分类成员, 而不是在实例被创建之后

# 在类定义时就执行初始化或者设置操作是元类的一个典型应用场景, 本质上讲一个元类会在定义时就被触发,这时候可以执行
# 一些额外的操作

# 下面的例子用于实现类似于collections中的命名元组的类

import operator

class StructTupleMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))

# type(clsname, (), {})
class StructTuple(tuple, metaclass=StructTupleMeta):
    _fields = []
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError('{} arguments required'.format(len(cls._fields)))
        return super().__new__(cls, args)

class Stock(StructTuple):
    _fields = ['name', 'shares', 'price']
# 在上面的例子中, 类StructTupleMeta获取到类属性_fields中的属性名, 然后将他们转换成相应的
# 可访问特定元组槽的方法, 函数operator.itemgetter()创建一个访问器函数, 然后property()函数
# 将其转换成一个属性

# 最难理解的地方:初始化步骤何时发生, StructTupleMeta中的__init__方法只在每个类被定义时调用一次
# cls参数就是被定义的类,
# StructTuple作为一个普通的基类, 供其他使用者来继承,

