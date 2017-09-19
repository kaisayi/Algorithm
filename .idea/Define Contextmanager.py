#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 实现一个上下文管理器, 以便使用with语句
# 方法: 使用contextlib模块中的@contextmanager

# 下面是实现代码块计时功能的上下文管理器

import time
from contextlib import contextmanager

@contextmanager
def timethis(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{}: {}'.format(label, end - start))

# Example use

with timethis('counting'):
    n = 100000
    while n > 0:
        n -= 1

# 在函数timethis中, yield之前的代码会在上下文管理器中作为__enter__方法执行
# 所有在yield之后的代码会作为__exit__方法执行, 如果出现异常, 异常会在yield
# 语句那里抛出

# 下面是一个更高级一点的上下文管理器, 实现了列表的某种事务

@contextmanager
def list_transaction(org_list):
    working = list(org_list)
    yield working
    org_list[:] = working

# 这段代码的作用是任何对于列表的修改只有当所有代码运行完成并且不出现异常的情况下才会生效

items = [1, 2, 3]
with list_transaction(items) as working:
    working.append(4)
    working.append(5)



# 问题: 在使用范围内执行某个代码片段, 并且希望在执行之后所有的结果都不可见

# 一个简单情景, 在全局命名空间内执行一个代码片段



# 问题: 写解析并分析python源代码的程序

# 方案: 利用ast模块, 将python源代码编译成一个可被分析的抽象语法树(AST):

import ast
ex = ast.parse('2 + 3 * 4 + x', mode='eval')
print(ex)
ast.dump(ex)

