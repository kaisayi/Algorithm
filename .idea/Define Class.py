#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 创建一个新的类对象, 需要考虑将类的定义源代码以字符串的形式发布出去, 并且使用
# 函数比如exec()执行,

# 方案: 使用函数types.new_class()初始化信的类对象, 需要做的是提供类的名字, 父类元组
# 关键字参数, 以及一个用成员变量填充类字典的回调函数

# Method
def __init__(self, name, shares, price):
    self.name = name
    self.shares = shares
    self.price = price

def cost(self):
    return self.shares * self.price

cls.dict = {
    '__init__': __init__,
    'cost': cost
}

import types

Stock = types.new_class('Stock', (), {}, lambda ns: ns.update(cls_dict))
Stock.__module__ = __name__


# 在代码的最后, 对Stock的__module__属性赋值, 每次当一个类被定义后, 它的__module__属性包含了
# 定义它的模块名, 这个名字用于生成__repr__方法的输出

# 如果想要创建的类需要不同的元类, 可以通过types.new_class的第三个参数传递,
# 第四个参数是一个用来接受命名空间的映射对象的函数, 通常是一个普通的字典, 但是它实际上是__prepare__
# 方法返回的任意对象,这个函数需要使用上面的update方法给命名空间增加内容

# 在很多时候如果能构造新的对象是很有用的, 例如 namedtuple

import operator, types, sys

def named_tuple(clsname, fieldnames):
    cls_dict = {name: property(operator.itemgetter(n))
                for n, name in enumerate(fieldnames)}

    def __new__(cls, *args):
        if len(args) != len(fieldnames):
            raise TypeError('Expected {} arguments'.format(len(fieldnames)))
        return tuple.__new__(cls, args)

    cls_dict['__new__'] = __new__

    cls = types.new_class(clsname, (tuple,), {},
                          lambda ns: ns.update(cls_dict))

    cls.__module__ = sys._getframe(1).f_globals['__name__']

    return cls

# 在本例中使用了一个所谓的框架魔法, 通过调用sys._getframe()来获取调用者的模块名

# 这项技术的重点是他对于元类的正确使用, 可以通过:
Stock = type('Stock', (), cls_dict)

# 定义一个类, 这种方法忽略了一些关键步骤, 比如对于元类中的__prepare__方法的调用
# 如果仅仅想执行准备步骤, 可以使用types.prepare_class