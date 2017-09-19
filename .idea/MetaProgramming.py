#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 元编程

# 1. 类也是对象, 可以进行下列操作
#   可以赋值给一个变量
#   可以进行拷贝操作
#   可以为它增加属性操作
#   可以将它作为函数参数传递

# 2. 动态创建类
#   利用type函数, 可以接受一个类的描述作为参数, 然后返回一个类
#   type(类名, 父类的元组(针对继承的情况可以为空), 包含属性的字典(名称和值))
myshinyclass = type('Shinyclass', (), {})
print(myshinyclass)

#   可以接受一个字典来为类定义属性, 也可以向另一个类继承,
#   可以为类增加方法,因此
'''
class Foo(FooPa):
    bar = True
    def echo_bar(self):
        return self.bar
#   可以利用type操作
Foo = type('Foo', (FooPa,), {'Bar': True, 'echo_bar': echo_bar})
'''

# 3. 什么是元类
#   元类是用于创建类的'东西', type就是一个元类, 元类又被称为类工厂, type就是python
#   的内建元类

# 3.1. __metaclass__属性
#   在创建一个类时, class Bar(object) , 类对象Bar还没有在内存中创建, python解释器会找到
#   __metaclass__, 如果在父类中找不到, 就会在模块层次中寻找, 在metaclass中就可以创建类

# 3.2. 创建自定义元类
#   元类的目的是为了创建类时, 能够自动改变类的
#   metaclass可以任意被调用, 如果在模块级别被定义, 会做用到模块中的所有的类, 例如

def Upper_attr(future_class, future_parents, future_attr):
    # for name, key in future_attr.items:
    attr = [(name.upper(), value) for name, value in future_attr.items()
            if not name.startswith('__')]
    uppercase_attr = dict(attr)
    return type(future_class, future_parents, uppercase_attr)



class Foo2:
    __metaclass__ = Upper_attr
    bar = 'bip'

print(hasattr(Foo2, 'bar'))

print(hasattr(Foo2, 'BAR'))



