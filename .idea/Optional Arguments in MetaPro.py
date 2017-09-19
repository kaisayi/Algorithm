#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 定义一个元类, 允许类定义时提供可选参数, 这样可以控制或配置类的创建过程

# 方案: 在定义类的时候, python允许使用metaclass关键字指定特定的元类, 例如使用抽象基类

from abc import ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def reaf(self, maxsize=None):
        pass

    @abstractmethod
    def write(self, data):
        pass


# 在自定义的元类中可以提供其他的关键字参数

class Spam(metaclass=MyMeta, debug=Ture, synchronize=True):
    pass

# 为了使元类支持这些关键字参数, 必须确保在__prepare__(), __new__(), __init__方法红使用强制性的关键字参数.

class MyMeta(type):
    #Optional
    @classmethod
    def __prepare__(metacls, name, bases, *, debug=False, synchronize=False):
        pass
        return super().__prepare__(name, bases)

    #Require
    def __new__(cls, name, bases, *, debug=False, synchronize=False):
        pass
        return super().__new__(cls, name, bases)

    def __init__(self, name, bases, *, debug=False, synchronize=False):
        pass
        super().__init__(name, bases)


# 给一个元类添加可选关键字参数需要完全弄懂类创建的所有步骤, 因为这些参数会传递给每一个相关的方法
# __prepare__方法所在的所有类定义开始执行前首先被调用, 用来创建类命名空间, 通常来说, 这个方法只是简单返回
# 一个字典或者其他的映射对象, __new__方法用来实例化最终的类对象, 他在类的主体被执行完之后开始执行
# __init__在最后被调用, 用来执行一些初始化的工作


