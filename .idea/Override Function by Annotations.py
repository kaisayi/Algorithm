#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 如何利用函数参数注解实现基于类型方法的重载,

# 实例

class Spam:
    def bar(self, x:int, y:int):
        print('Bar1:', x, y)

    def bar(self, s:str, n:int = 0):
        print('Bar2:', s, n)


# 下面是一个具体的实例, 使用到了元类和描述器

import inspect, types

class MultiMethod:
    '''
    Represent a single multimethod
    '''

    def __init__(self, name):
        self._methods = {}
        self.__name__ = name

    def register(self, meth):
        '''
        register a new method as a multimethod
        :param meth:
        :return:
        '''
        sig = inspect.Signature(meth)
        # build a type signature from the method annotations
        types = []
        for name, parm in sig.parameters.items():
            if name == 'self':
                continue
            if parm.annotation is inspect.Parameter.empty:
                raise TypeError(
                    'Argument {} must be annotated with a type'.format(name)
                )
            if not isinstance(parm.annotation, type):
                raise TypeError(
                    'Argument {} annotation must be a type'.format(name)
                )
            if parm.default is not inspect.Parameter.empty:
                self._methods[tuple(types)] = meth
            types.append(parm.annotation)

        self._methods[tuple(types)] = meth

    def __call__(self, *args):
        '''
        call a method based on type signature of arguments
        :param args:
        :return:
        '''
        types = tuple(type(arg) for arg in args[1:])
        meth = self._methods.get(types, None)
        if meth:
            return meth(*args)

