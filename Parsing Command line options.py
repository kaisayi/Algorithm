#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# 问题: 程序解析命令行选项(位于sys.argv中)

# argparse模块可以被用来解析命令行选项,

'''
Hypothetical command-line tool for searching a collection of files for one or more text patterns
'''

import argparse

parser = argparse.ArgumentParser(description='Searching some files')

parser.add_argument(dest='filename', metavar='filename', nargs='*')

parser.add_argument('-p', '--pat', metavar='pattern', required=True,
                    dest='patterns', action='append',
                    help='text pattern to search for')

parser.add_argument('-v', dest='verbose', action='store_true',
                    help='verbose mode')

parser.add_argument('-o', dest='outfile', action='store',
                    help='output file')

parser.add_argument('--speed', dest='speed', action='store',
                    choices={'slow', 'fast'}, default='slow',
                    help='search speed')

args = parser.parse_args()


# 在add_arguments()调用中, dest参数指定解析结果被指派给属性的名字,
# metavar参数被用来生成帮助信息, action参数指定跟属性对应的处理逻辑, 通常为store
# 被用来存储某个值或将多个参数值收集到一个列表中

# 需求: 写一个脚本, 运行时需要一个密码, 脚本是交互式的, 因此不能将密码在脚本中硬编码, 而是需要弹出
# 一个密码提示

# 解决方案: getpass模块,

import getpass

user = getpass.getuser()
passwd = getpass.getpass()
if svc_login(user, passwd):    # you must write svc_login()
    print('Yay')
else:
    print('Boo')

# 在此代码中, svc_login是你要实现的处理密码的函数


# 需求: 获取终端的大小, 以便正确的格式化输出


# 需求: 执行一个外部命令并且以python字符串的形式获取执行结果

# 方案: 使用subprocessing.check_output函数

import subprocess
out_bytes = subprocess.check_output(['netstat', '-a'])

# 这段代码执行一个指定的命令并将执行结果以一个字节字符传的形式返回, 如果需要以文本形式返回

out_text = out_bytes.decode('utf-8')

# 通常情况下, check_output仅仅返回输入到标准输出的值, 如果需要同时收集标准输出和错误输出,使用stderr

out_bytes = subprocess.check_output(['cmd', 'arg1', 'arg2'],
                                    stderr=subprocess.STDOUT)

# 如果需要使用一个超时机制,来执行, 使用timeout
