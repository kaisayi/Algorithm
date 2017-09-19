#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# Problem: you want a script you've write to be able to accept input using whatever
# mechanism is easiest for the user, this should include piping output from a command
# to the script redirecting a file into the script, or just passing a filename, or list
# of a filenames, to the script on the command line

# solution: fileinput module makes this very simple and consice. if you have a script like this

import fileinput

with fileinput.input() as f_input:
    for line in f_input:
        print(line, end='')

# fileinput.input()创建并返回一个FileInput类的实例, 该实例除了拥有一些有用的帮助方法之外,
# 还可以被当作一个上下文管理器使用, 如果要写一个打印多个文件输出的脚本, 那么需要在输出的时候包含文件名和行号

with fileinput.input('/etc/passwd') as f:
    for line in f:
        print(f.filename(), f.lineno(), line, end='')

# 通常将它作为一个上下文管理器是哟码嗯,可以确保它不再使用时, 文件自动关闭,