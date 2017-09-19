#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 想在函数上添加一个包装器, 增加额外的操作处理

# 使用装饰器


import time
from functools import wraps

def timethis(func):
    '''
    decorator that reports the execution time
    :param func:
    :return:
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result
    return wrapper

@timethis
def countdown(n):
    '''
    counts down
    :param n:
    :return:
    '''

    while n > 0:
        n -= 1

# countdown(190000)

# 需要强调的是装饰器并不会修改原始函数的参数签名和返回值, 使用*args和**kwargs的目的是所有的参数都能使用
# @wraps(func)的原因是: 保留原始函数的元数据,


