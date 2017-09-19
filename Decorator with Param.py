#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题 : 定义一个带参数的装饰器
# 假如需要给函数添加日志功能, 同时允许用户指定日志的级别和其他选项

from functools import wraps
import logging

def logged(level, name=None, message=None):
    '''
    add logging to a function
    :param level: logging level
    :param name: logger name
    :param message: log message, if name and message are not specified they default to the
    function's module and name
    :return:
    '''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        return wrapper

    return decorate

@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def Spam():
    print('Spam!')

'''
@decorator(x, y, z)
def func(a, b):
    pass

# 和下面的过程是等效的

def func(a, b):
    pass
func = decorator(x, y, z)(func)



# The User-Defined Properties Decorator

# 问题: 想用一个装饰器包装一个函数, 并且允许用户提供参数在运行时控制装饰器行为

# 方案: 引入访问函数, 使用nonlocal修改内部变量, 然后这个访问函数作为一个属性值赋值给包装函数
'''
from functools import partial, wraps
import logging

# Utility decorator to attach a function as an arribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func

def logged(level, name=None, message=None):
    '''
        add logging to a function
        :param level: logging level
        :param name: logger name
        :param message: log message, if name and message are not specified they default to the
        function's module and name
        :return:
        '''

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper
    return decorate

# attach_wrapper(wrapper, set_level) => (wrapper.set_level) = set_level =>

# 这一小结的关键点是访问函数, 它们被作为属性赋值给包装器, 每个访问函数允许使用nonlocal修改内部的变量

# 还有一点: 访问函数会在多层装饰器间传播(如果装饰器都使用了@wraps), 假设如下:
@timethis
@logged(logging.DEBUG)
def countdown(n):
    while n > 0:
        n -= 1

# 访问函数依然有效, timethis和logged相反顺序效果一样
# 还能通过lambda表达式来让访问函数返回不同的设定值

@attach_wrapper(wrapper)
def get_level():
    return level

# alternative
wrapper.get_level = lambda: level


# 还有一种a方法直接访问函数的属性

@wraps(func)
def wrapper(*args, **kwargs):
    wrapper.log.log(wrapper.level, wrapper.logmsg)
    return func(*args, **kwargs)

# attach adjustable attributes
wrapper.level = level
wrapper.logmsg = logmsg
wrapper.log = log
# 这个方法也能正常工作, 但是前提是它必须是最外层的装饰器, 如果上面还有装饰器, 那么会隐藏底层的属性,
# 使得修改它们没有任何作用, 通过访问函数可以避免


# 问题: 实现一个装饰器, 既可以不传参数, 也可以传参数

# 解决方案:

from functools import partial
import logging

def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper

#example use

@logged
def add(x, y):
    return x + y

@logged(level=logging.CRITICAL, name='example')
def Spam():
    print('Spam')

