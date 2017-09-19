#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 让某个类支持标准的比较操作(>= != <= <), 但是不想实现一堆方法

# 装饰器functools.total_ordering 就是用来简化处理, 只需要定义一个__eq__方法和(__lt__, __le__, __ge__, __gt__)
# 任意一个

from functools import total_ordering

class room:
    def __init__(self, name, length, width):
        self.name = name
        self.lenth = length
        self.width = width
        self.square_feet = self.lenth * self.width

@total_ordering
class House:
    def __init__(self, name, style):
        self.name = name
        self.style = style
        self.rooms = []

    @property
    def living_space_footage(self):
        return sum(room.square_feet for room in self.rooms )

    def add_room(self, room):
        self.rooms.append(room)

    def __str__(self):
        return '{}: {} square foot {}'.format(self.name,
                                              self.living_space_footage,
                                              self.style)

    def __eq__(self, other):
        return self.living_space_footage == other.living_space_footage

    def __lt__(self, other):
        return self.living_space_footage < other.living_space_footage


h1 = House('h1', 'Foral')
h1.add_room(room('Master', 12, 32))
h1.add_room(room('Sester', 8, 12))
h1.add_room(room('Hadder', 14, 22))
h2 = House('h2', 'England')
h2.add_room(room('Jodal', 23, 11))
h2.add_room(room('Maple', 42, 3))
print(h1 < h2)

# total_ordering 的实现: 定义一个从每个比较支持方法到所需要定义的其他方法的一个映射,
# 比如定义了__le__()方法, 就被用来构建其他的方法
