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
        return 'Node({!r:})'.format(self.value)

    # property that manages the parent as a weak-reference
    @property
    def parent(self):
        return None if self._parent is None else self._parent()

    @parent.setter
    def parent(self, Node):


