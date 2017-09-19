#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 在创建一个类的对象时, 如果之前使用过相同参数创建过这个对象, 则返回它的缓存应用

# 方法: 单例模式, 比如logging模块, 使用相同名创建的logger实例永远只有一个

import logging
# a = logging.getLogger('foo')
# b = logging.getLogger('bar')

# print(a is b)
# c = logging.getLogger('foo')
# print(a is c)

# 为了达到这个效果, 需要使用一个和类本身分开的工厂函数

# The class in question
class Spam:
    def __init__(self, name):
        self.name = name

# Caching support

import weakref
_spam_cache = weakref.WeakValueDictionary()

def get_Spam(name):
    if name not in _spam_cache:
        s = Spam(name)
        _spam_cache[name] = s
    else:
        s = _spam_cache[name]
    return s


# weakref 模块
# A primary use for weak references is to implement caches or mappings holding large objects,
# where it’s desired that a large object not be kept alive solely because it appears in a cache or mapping.

# For example, if you have a number of large binary image objects,
# you may wish to associate a name with each. If you used a Python dictionary to
# map names to images, or images to names, the image objects would remain alive
# just because they appeared as values or keys in the dictionaries. The WeakKeyDictionary
# and WeakValueDictionary classes supplied by the weakref module are an alternative,
# using weak references to construct mappings that don’t keep objects alive solely
# because they appear in the mapping objects. If, for example, an image object is a value
# in a WeakValueDictionary, then when the last remaining references to that image object
# are the weak references held by weak mappings, garbage collection can reclaim the object,
# and its corresponding entries in weak mappings are simply deleted.

# 除了工厂函数之外, 还可以使用__new__方法

class Spam2:
    _spam_cache2 = weakref.WeakValueDictionary()
    def __new__(cls, name):
        if name in cls._spam_cache2:
            return cls._spam_cache2[name]
        else:
            self = super.__new__(cls)
            cls._spam_cache2[name] = self
            return self
    def __init__(self, name):
        print('Initializing Spam')
        self.name = name

# 这样导致的问题是每次__init__()方法就会被调用, 不管实例是否被缓存

# 在保存实例缓存时, 如果只想在程序使用时才保存, 一个WeakValueDictionary实例只会保存那些还在被使用的实例
# 否则只要实例不再使用, 就会从字典中移除

# 更加高级的实现
# 使用一个全局变量, 并且工厂函数和类放在一起, 可以通过缓存代码放到一个单独的缓存管理器中,
import weakref
class CachedSpamManager:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            s = Spam3(name)
            self._cache[name] = s
        else:
            s = self._cache[name]

        return s

    def clear(self):
        self._cache.clear()

class Spam3:
    manager = CachedSpamManager()
    def __init__(self, name):
        self.name = name

    @classmethod
    def get_spam(cls, name):
        return cls.manager.get_spam(name)

# 这样用户可以直接实例化这个类, 而出现重复对象, 有几种方式可以防止用户这样做,
# 第一个将类的名字修改为以下划线开头, 提示以用户别直接调用
# 第二种方式 就是让这个类的__init__方法抛出异常

# 最后的修正:

class CachedSpamManager2:
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()

    def get_spam(self, name):
        if name not in self._cache:
            temp = Spam4._new(name)
            self._cache[name] = temp
        else:
            temp = self._cache[name]

        return temp

    def clear(self):
        self._cache.clear()

class Spam4:
    def __init__(self):
        raise RuntimeError('Cannot instantiate directly')

    @classmethod
    def _new(cls, name):
        self = cls.__new__(cls)
        self.name = name
        return self