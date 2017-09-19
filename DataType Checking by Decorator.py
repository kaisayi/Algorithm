#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 作为某种编程规定, 需要对函数参数进行强制类型检查

# 目标: 能对函数参数类型进行断言
'''
@typeassert(int, int)
def add(x, y):
    return x + y
'''
# 实现typeassert

from inspect import signature
from functools import wraps


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguements

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(value, bound_types[name])
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorate


# 这个装饰器既可以指定所有参数类型, 也可以指定部分, 并且可以通过位置或者关键字来指定参数类型

@typeassert(int, z=int)
def Spam(x, y, z=3):
    print(x, y, z)


#  这一节引入的概念
# 装饰器只会在函数中被调用一次, 想要去掉装饰器的功能, 只需要简单返回被装饰的函数
# 在下面的代码中, 如果全局变量__debug__被设置成了false(使用-o, 或者-oo参数的优化模式执行程序)
# 就直接返回函数本身

def docorate(func):
    if not __debug__:
        return func

# 对函数签名检查, 使用inspect.signature函数, 它运行提取一个可调用对象的参数签名信息,
# 装饰器,使用了bind_partial来执行从指定类型到名称的绑定,




