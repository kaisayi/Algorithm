#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''
import math
from math import pi as PI
from itertools import permutations
from pprint import pprint
import logging


FLIGHTH = 1.2
VIC = 60
ALLOW_TIME = 4
SCAN_WIDTH = 2 * FLIGHTH * math.tan(PI/6)

class Queue:
    def __init__(self):
        self._items = []

    def dequeue(self):
        return self._items.pop()

    def enqueue(self, item):
        self._items.insert(0, item)

    def isEmpty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

# class OrderedList:
#
#     def __init__(self):
#         self._items = []
#
#     def addItem(self, item):
#         i = 0
#         size = len(self._items)
#         found = False
#         while i < size and not found:
#             if item < self._items[i]:
#                 self._items.insert(i, item)
#                 found = True
#         if not found:
#             self._items.append(item)
#
#     def __str__(self):
#         return str(self._items)
#
# d = OrderedList()
# d.addItem(23)
# d.addItem(2)
# d.addItem(33)
# d.addItem(13)
# d.addItem(29)
# d.addItem(24)
# print(d)




class Node:

    def __init__(self, name, x, y, delay=0):
        self.name = name
        self.x = x
        self.y = y
        # self.area = area
        self.connetions = []
        self.delay = delay
        self.hasVisit = False


    def getDelay(self):
        return self.delay

    def setDelay(self, newdelay):
        self.delay = newdelay

    # def delay(self, width=SCAN_WIDTH):
    #     return self.area/(width * VIC)

    def addConnections(self, node):
        self.connetions.append(node)

    def getDistance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __str__(self):
        return 'Node{} delay{}'.format(self.name, self.delay)

    def Visit(self):
        self.hasVisit = True



class Vertex:

    def __init__(self):
        self.current = None
        self.connectedTo = []

    def addConnections(self, node):
        self.connectedTo.append(node)


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance

@singleton
class Graph:
    _start_x = 110
    _start_y = 0
    _start = Node('H', _start_x, _start_y)
    def __init__(self):
        self.verList = [self._start,]
        # self.connectedTo = {}
        self.numVertices = 1
        self.logger = logging.getLogger()

    def getVertex(self, i):
        return self.verList[i]

    def addVertex(self, *args):
        newVertex = Node(*args)
        # self.verList.append(newVertex)
        for vertex in self.verList:
            vertex.addConnections(newVertex)
            newVertex.addConnections(vertex)
        self.numVertices += 1
        self.verList.append(newVertex)

    def delVertex(self, ):
        pass

    # def chVertex(self, vert, newarea):


    def getPath(self):

        return permutations(self.verList[1:])

    def getMaxScanTime(self):
        pathList = {}
        for path in self.getPath():
            current = self._start
            arrive_time= 0
            scan_time = 0
            subpath = []
            for vert in path:
                # scan_time += vert.delay()
                # whole_time = whole_time + current.getDistance(vert)/VIC + vert.delay()
                # current = vert
                # subpath.append(vert.name)
                if arrive_time > ALLOW_TIME:
                    # remainArea = 2 * FLIGHTH*math.tan(PI/6) * VIC * (time - ALLOW_TIME)
                    # scan_time -= (whole_time - ALLOW_TIME)
                    break
                # time = t
                elif arrive_time + current.delay > ALLOW_TIME:
                    scan_time += (ALLOW_TIME - arrive_time)
                    break
                else:
                    scan_time += current.delay
                    arrive_time += (current.delay + current.getDistance(vert)/VIC)
                    current = vert
                    subpath.append(current)


            subpath = tuple(subpath)
            pathList[subpath] = scan_time
        # print(pathList)
        # pprint(pathList)

        pathList = sorted([*pathList.items()], key= lambda x: x[-1], reverse=True)
        # return pathList
        return pathList[0]

    # def VerifyPath(self):
    #     pass

    def chGraph(self):
        path, time = self.getMaxScanTime()
        print([ver.name for ver in path])
        for ver in path:
            if ver.delay <= time:
                time -= ver.delay
                ver.setDelay(0)
            else:
                remain_time = ver.delay - time
                ver.setDelay(remain_time)
        return [ver.delay for ver in self.verList[1:]]


    def loopVisit(self):
        origin_delay = [vertex.delay if vertex.delay > float('0') else float('1.0')
                       for vertex in self.verList[1:]]
        print(origin_delay)
        Coverage = float('0')
        while Coverage < float('0.99'):
            newList = self.chGraph()
            print(newList)
            Coverage = 1 - sum(newList[i]/origin_delay[i] for i in range(len(newList)))/len(newList)
            print(Coverage)








    # def bfsVisit(self):
    #     visitPath = []
    #     vertQueue = Queue()
    #     vertQueue.enqueue(self._start)
    #     Finished = False
    #     while vertQueue.size() > 0 and not Finished:
    #         currentVertex = vertQueue.dequeue()
    #         visitPath.append(currentVertex)
    #         for nbr in currentVertex.connections:
    #             if not nbr.hasVisit and nbr != self._start:
    #                 nbr.Visit()
    #                 vertQueue.enqueue(nbr)
    #             elif nbr == self._start:
    #                 Finished = True


    # def gVisit(self, current, visited):
    #     for nbr in current.connections:
    #
    #     for i in range(self.numVertices):
    #         if
    #
    # def bfsVisit(self):
    #     # i = self.numVertices
    #     pathList = [self._start]
    #     current = self._start
    #     Finished = False
    #     while len(pathList) < self.numVertices and not Finished:
    #         for nbr in current.connetions:
    #             if nbr == self._start:
    #                 Finished = True
    #                 break
    #             pathList.append(nbr)
    #             current
    #
    # def DFSTraverse(self):
    #     visited = [False]*self.numVertices
    #     for i in range(self.numVertices):
    #         if not visited[i]:
    #             DFS(i)
    #
    #     def DFS(i):
    #         visited[i] = True
    #         for ver in self.verList[i].connetions:
    #             if
    #
    # def verTraverse(self):
    #     visited = []
    #     n = self.numVertices
    #
    #     def nextVer(current_num, step):
    #         if step == n:
    #             yield visited

POS = [['A', 30.3, 89.9,  2.07],
       ['B',66.0, 84.7, 3.38],
       ['C',98.4, 76.7, 2.33],
       ['D',73.7, 61.0, 1.73],
       ['E',57.9, 47.6, 2.61],
       ['F',86.8, 22.0, ],
       ['G',93.6, 48.8, 0.01]
       ]

G = Graph()
for p in POS:
    G.addVertex(*p)

# pprint(G.getMaxScanTime())
G.loopVisit()
# for i in range(10):
#     print(G.chGraph())


# for p in G.verList:
#     dis = [(p.getDistance(other), other.name) for other in p.connetions]
#     print(p.name, dis)














