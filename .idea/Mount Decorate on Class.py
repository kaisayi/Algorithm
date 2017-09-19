#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 在类中定义装饰器, 并将其作用在其他的函数或者方法上

# 解决方法: 确定装饰器的使用方法, 到底是作为一个实例方法还是类方法, 下面是一个例子
# 对比实例方法和类方法的区别

from functools import wraps

class A:
    # Decorator as an instance method
    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorate1')
            return func(*args, **kwargs)
        return wrapper

    # Decorator as an class method
    @classmethod
    def decorator2(cls, func):
        @warps(func)
        def wrapper(*args, **kwargs):
            print('Decorate2')
            return func(*args, **kwargs)
        return wrapper

# 下面是一组例子
a = A()
@a.decorator1
def Spam():
    pass

@A.decorator2
def grok():
    pass


# 两者一个是实例调用, 一个是类调用
# 在类中定义装饰器, 在标准库中也有很多例子, @property装饰器实际上就是一个类
# 它定义了三个方法getter(), setter(), deleter(), 每一个方法都是一个装饰器

class Person:
    # Create a property instance
    first_name = property()

    # apply decorator method
    @first_name.getter
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self):
        if not isinstance(value, str):
            raise TypeError('Expect a string')
        self._first_name = value


# 这样定义的主要原因是, 各种不同的装饰器方法会在关联的property实例上操作它的状态
# 因此任何时候只要碰到需要在装饰器中记录或者绑定信息, 都可使用

# 在类中定义装饰器难以理解的地方是对于额外参数self和cls的正确使用, 这个参数尽在你需要访问
# 包装器中的某个实例的某些部分的时候使用

# 对于类中的包装器在涉及继承的时候, 比如需要在A 中的装饰器继承到B中,

class B(A):
    @A.decorator2
    def bar(self):
        pass


# Defining the Decorator as Class

# 问题: 使用一个装饰器包装函数, 但希望得到一个可调用的实例, 需要让装饰器可以同时工作在类定义的内部和外部

# 解决方法: 将装饰器定义成实例, 需要确保实现了__call__ 和 __get__,

import types
from functools import wraps

class Profiled:
    def __init__(self, func):
        warps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)

# 将装饰器定义成类的细节
# 首先, 使用functools.wraps(), 将被包装函数的元信息复制到可调用的实例中去,
# 其次, 通常容易忽略上面的__get__方法, 会出现问题, 原因是当方法函数在一个类中被查找时, 它们的__get__方法
# 依据描述器协议被调用, 在这里__get__的目的是创建一个绑定方法对象(最终会给这个方法传递self参数)例如

class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)

s = Spam()
def grok(self, x):
    pass

grok.__get__(s, Spam)

# __get__方法是为了确保绑定方法对象能够被正确的创建, type.MethodType()手动创建一个绑定的方法
# 使用, 只有当实例被使用时绑定的方法才会被创建, 如果这个方法在类上面来访问, 那么__get__中的instance
# 参数会被设置成None, 并且直接返回Profiled实例本身, 这样就可以提取ncalls属性了,

# 如果想避免一些混乱, 可以考虑闭包,和nonlocal变量实现的装饰器,

import types
from functools import wraps

def profiled(func):
    ncalls = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal ncalls
        ncalls += 1
        return func(*args, **kwargs)

    wrapper.ncalls = lambda : ncalls
    return wrapper

# Example
@Profiled
def add(x, y):
    return x + y


