#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 处理大量的不同对象组成的复杂数据结构, 每个对象需要进行不同的处理, 比如遍历一个树结构
# 然后根据每个节点的相应状态执行不同的操作

# 通过访问者模式,假如要写一个数学表达式:

class Node:
    pass

class UnaryOperator(Node):
    def __init__(self, Operand):
        self.operand = Operand


class BinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Negate(UnaryOperator):
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value

# 利用这些类来构建数据结构
# 但是问题是每个表达式都需要重新定义一遍, 通用的方式让它支持所有的数字和操作符号, 便可以使用访问模式

class NodeVisitor:
    def visit(self, node):
        methname = 'visit' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))

# 为了使用这个类, 可以定义一个类继承并实现各种visit方法

class Evaluator(NodeVisitor):

    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        return node.visit(node.left) + node.visit(node.right)

    def visit_Sub(self, node):
        return node.visit(node.left) + node.visit(node.right)

    def visit_Mul(self, node):
        return node.visit(node.left) * node.visit(node.right)

    def visit_Div(self, node):
        return node.visit(node.left) / node.visit(node.right)

    def visit_Negate(self, node):
        return node.visit(node.operand)

# 下面定义一个类在一个栈上将一个表达式转换成多个操作序列

class StackCode(NodeVisitor):
    def generate_code(self, node):
        self.instructions = []
        self.visit(node)
        return self.instructions

    def visit_Number(self, node):
        self.instructions.append(('PUSH', node.value))

    def binop(self, node, instruction):
        self.visit(node.left)
        self.visit(node.right)
        self.instructions.append((instruction))

    def visit_Add(self, node):
        self.binop(node, 'ADD')

    def visit_Sub(self, node):
        self.binop(node, 'SUB')

    def visit_Mul(self, node):
        self.binop(node, 'MUL')

    def visit_Div(self, node):
        self.binop(node, 'DIV')

    def unaryop(self, node, instruction):
        self.visit(node.operand)
        self.instructions.append(instruction)

    def visit_Nagate(self, node):
        self.unaryop(node, 'NEG')



# 这种技术是实现其它语言中的switch语句, 比如正在写以一个http框架, 需要一个请求分发的控制器

class HTTPHandler:
    def handle(self, request):
        methname = 'do_' + request.request_method
        getattr(self, methname)(request)

    def do_GET(self, request):
        pass

    def do_POST(self, request):
        pass

    def do_HEAD(self, request):
        pass

# 访问者模式的一个缺点是严重依赖递归, 层次太深会超出python递归深度限制

# 非递归实现访问者模式

# 解决方式: 使用生成器可以在树遍历或者搜索算法中消除递归
# 利用一个栈和生成器实现这个类

import types

class NodeVisitor2:
    def visit(self, node):
        stack = [node]
        last_result = None
        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    stack.append(last.send(last_result))
                    last_result = None
                elif isinstance(last, Node):
                    stack.append(self._visit(stack.pop()))
                else:
                    last_result = stack.pop()
            except StopIteration:
                stack.pop()

        return last_result

    def _visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))

if __name__ == '__main__':
    for i in range(10000):
        a = Add()






