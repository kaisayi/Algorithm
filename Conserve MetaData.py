#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 写一个装饰器作用在函数上, 这个函数的重要元信息如名字, 文档字符串, 注解和参数签名丢失

# 在任何时候, 定义装饰器, 应该使用functools中的@wraps来包装函数

# @wrapsi还有一个重要的特性是, 通过属性__wraps__直接访问包装函数,


# 问题: 装饰器已经作用在一个函数上, 想要撤销, 直接访问未包装的函数

# 方案: 假设装饰器通过@wraps实现, 可以通过__wrapped__属性访问

'''
@somedecorator
def add(x, y):
    return x + y

orig_add = add.__wrapped__
'''
# 假如有较多个装饰器, 那么访问__wrapped__属性的行为是不可预知的, 应该避免这么做
# 在python3.3中, 它会略过所有的包装层, 比如:

from functools import wraps

def decorator1(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 1')
        return func(*args, **kwargs)

    return wrapper

def decorator2(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 2')
        return func(*args, **kwargs)

    return wrapper

@decorator1
@decorator2
def add(x, y):
    return x + y

print(add(2, 5))

print(add.__wrapped__(2, 5))

# 并不是所有的装饰器都使用了@wraps, 因此这里的方案并不全都适用, 特别的, 内置的装饰器@staticmethod
# 和@classmethod就没有遵循这个约定, 它们把原始函数存储在属性__func__