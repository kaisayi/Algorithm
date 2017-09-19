#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 想通过改变实例创建方式实现单例\缓存\其他特性

# 在python中, 定义一个类可以像函数一样调用它创建实例,
# 如果向自定义调用函数, 需要重写__call__方法
# 如果不想任何人创建这个类的实例

class NoInstance(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("can not instantiate directly")

class Spam(metaclass=NoInstance):
    @staticmethod
    def grok(x):
        print('Spam.grok')



# 问题: 自动记录一个类中的属性和方法定义的顺序, 然后可以利用它来做多种操作
# 比如: 序列化, 映射到数据库

# 解决方法: 利用元类, 下面一个例子使用了Orderdict记录描述器的定义顺序

from collections import OrderedDict
# A set of descriptions for various types
class Typed:
    _expect_type = type(None)
    def __init__(self, name=None):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, self._expect_type):
            raise TypeError('Expect ' + str(self._expect_type))
        instance.__dict__[self.name] = value

class Integer(Typed):
    _expect_type = int


class String(Typed):
    _expect_type = str

class Float(Typed):
    _expect_type = float

class OrderedMeta(type):

    def __new__(cls, classname, bases, clsdict):
        d = dict(clsdict)
        order = []
        for name, value in clsdict.items():
            if isinstance(vaTyped):
                value._name = name
                order.append(name)
        d['_order'] = order
        return type.__new__(cls, clsname, bases, d)

    @classmethod
    def __perpare__(cls, claname, bases):
        return OrderedDict()

# 在这个元类中, 执行主体时描述器的定义顺序会被一个
# OrderDict捕获到, 生成的有序名称从字典中提取出来并放入类属性_order中

# 本节的关键点是OrderedMeta中定义的__prepare__方法, 这个方法会在开始定义类和它的父类的时候执行,
# 他必须返回一个映射对象以便在类定义中被使用到,
# 想要构造自己的类字典对象, 可以扩展这个功能, 下面这个例子可以防止重复的定义

from collections import OrderedDict
class NoDupOrderDict(OrderedDict):

    def __init__(self, clsname):
        self.clsname = clsname
        super().__init__()

    def __setitem__(self, key, value):
        if key in self:
            raise TypeError('{} already defined in {}'.format(key, self.clsname))

        super().__setitem__(key, value)

class OrderedMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        d['_order'] = [name for name in clsdict if name[0] != '_']
        return type.__new__(cls, clsname, bases, clsdict)

    @classmethod
    def __prepare__(metacls, clsname, bases):
        return NoDupOrderDict(clsname)

class A(metaclass=OrderedMeta):
    def Spam(self):
        pass


# A => OrderedMeta(create an class instance) => __new__() => prepare(clsdict) => new class

# 在__new__方法对于元类中被修改字典的处理, 尽管类使用了另外的字典定义, 在构造最终的class对象的时候, 仍然需要
# 将这个字典转换为一个正确的dict实例,
