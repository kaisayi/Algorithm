#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

#  问题: 程序创建了很多循环引用数据结构(树, 图, 观察者模式), 出现内存管理的问题
# 解决方法: 循环引用数据结构, 一个简单的例子是树形结构, 双亲指针指向孩子节点, 孩子节点又返回指向双亲节点,
# 可以使用weakref库中的若引用

import weakref


class Node:
    def __init__(self, value):
        self.value = value
        self._parent = None
        self.children = []

    def __repr__(self):
        return 'Node({!r})'.format(self.value)

    # property that manages the parent as a weak-reference
    @property
    def parent(self):
        return None if self._parent is None else self._parent

    @parent.setter
    def parent(self, node):
        self._parent = weakref.ref(node)

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


# root = Node('parent')
# c1 = Node('child')
# root.add_child(c1)
# print(c1.parent)

# 循环引用数据结构在python中是一个棘手的问题, 因为正常的 垃圾回收机制不能适用于这种情况,例如:

# class just to illustrate when delete occurs

class Data:
    def __del__(self):
        print('Data.__del__')


# node class involving a cycle
class Node2:
    def __init__(self):
        self.data = Data()
        self.parent = None
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


# 下面是垃圾回收实验
a = Data()
del a  # immediately deleted
a = Node2()
del a  # immediatey deleted
a = Node2()
a.add_child(Node2())
del a  # Not deleted(no message)

# 最后一个删除时打印语句没有出现， 原因是python的垃圾回收机制基于简单的引用计数
# 可以手动触发

# +BEGIN_SRC python

import gc

gc.collect()  # force collection


# Data.__del__
# Data.__del__
# +END_SRC

# 如果循环引用的对象还定义了自己的__del__方法，情况会比较糟糕

# +BEGIN_SRC python
# Node class involving a cycle
class Node:
    def __init__(self):
        self.data = Data()
        self.parent = None
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    # Never define like this
    # only here to illustrate pathological behavior
    def __del__(self):
        del self.data
        del self.parent
        del self.children

# +END_SRC

# 在这种情况下, 垃圾回收 永远不会回收这个对象,
# 弱引用消除了引用循环的这个问题, 本质上来说, 弱引用是一个对象指针, 它不会增加
# 引用次数, 可以通过weakref创建弱引用

a = Node2()
a_ref = weakref.ref(a)

# 为了访问弱引用所引用的对象, 可以像函数一样调用, 如果对象还存在就返回它, 不存在就返回None


