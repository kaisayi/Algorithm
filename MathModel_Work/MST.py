#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

import math
from inspect import signature
from functools import wraps
from pprint import pprint

TARFILE = 'target.txt'
# TAR_R = 3
RELAY_R = 6
TAR_R = 1


def typeAssert(*ty_args, **ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func

        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Arguement {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs)

        return wrapper

    return decorate


def loadFromFile(filename):
    with open(filename, 'r+') as f:
        while True:
            x = f.readline().strip()
            y = f.readline().strip()
            yield (x, y)
            if x == '':
                break


def Floatfy(alist):
    return [float(i) for i in alist]


class Vertex:
    _x = float('0')
    _y = float('0')

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.Prt = None
        self.Chld = None

    def getDistance(self, other):
        return math.sqrt((self._x - other._x) ** 2 + (self._y - other._y) ** 2)

    # def addConnection(self, other):
    #     self.connectedTo.append(other)

    def MidNode(self, other):
        mid_x = (self._x + other._x) / 2
        mid_y = (self._y + other._y) / 2
        return Vertex(mid_x, mid_y)

    def __str__(self):
        return 'node({},{})'.format(self._x, self._y)

class matGraph:
    def __init__(self):
        self.vertexList = []
        self.AdjMatrix = []
        # self.numVertex = 0

    def initGraph(self):
        for item in loadFromFile(TARFILE):
            if not item[0]:
                break
            vert = Vertex(*Floatfy(item))
            self.addEdge(vert)
            self.vertexList.append(vert)

    def addEdge(self, newVertex):
        if len(self.vertexList) == 0:
            self.AdjMatrix.append([0])

        else:
            dList = []
            for i in range(len(self.vertexList)):
                currentVertex = self.vertexList[i]
                d = currentVertex.getDistance(newVertex)
                dList.append(d)
                self.AdjMatrix[i].append(d)
            dList.append(0)
            self.AdjMatrix.append(dList)

    def getXRange(self):
        x_min = min(vert._x for vert in self.vertexList)
        x_max = max(vert._x for vert in self.vertexList)
        return x_min, x_max

    def InDiskVertex(self, center, radius):
        indiskList = []
        for vertex in self.vertexList:
            if center.getDistance(vertex) < radius+1e-4:
                indiskList.append(vertex)

        return indiskList

    # get the mini span tree using Prim
    def MSpanTree(self):
        TreeU = [self.vertexList[0], ]
        closEdge = [0]
        # init the array
        for i in range(1, len(self.vertexList)):
            closEdge.append(self.AdjMatrix[0][i])
            self.vertexList[i].Prt = self.vertexList[0]
            self.vertexList[0].Chld = self.vertexList[i]

        while len(TreeU) < len(self.vertexList):
            minValue = min(closEdge, key=lambda x: x if x > 0 else float('inf'))
            minIndex = closEdge.index(minValue)
            currentVert = self.vertexList[minIndex]
            TreeU.append(currentVert)
            for i in range(len(closEdge)):
                if i == minIndex:
                    closEdge[i] = 0
                elif currentVert.getDistance(self.vertexList[i]) < closEdge[i]:
                    closEdge[i] = currentVert.getDistance(self.vertexList[i])
                    self.vertexList[i].Prt = currentVert
                    currentVert.Chld = self.vertexList[i]

        return TreeU

    # Single-Tiered Relay Node Placement
    def STRNP(self):
        relayList = []
        MSTList = self.MSpanTree()

        # separte the line when the length longer than 2*TAR_R
        def sepline(vert1, vert2, chord):
            # sepList = []
            sin_theta = (vert2._y - vert1._y) / chord
            cos_theta = (vert2._x - vert1._x) / chord
            sVert = Vertex(vert1._x + TAR_R * cos_theta, vert1._y + TAR_R * sin_theta)
            eVert = Vertex(vert2._x - TAR_R * cos_theta, vert2._y - TAR_R * sin_theta)
            relayList.extend([sVert, eVert])

            s_to_e = sVert.getDistance(eVert)
            # print(s_to_e)
            parts = int(math.ceil(s_to_e / RELAY_R))
            sli = [
                Vertex((sVert._x * i + eVert._x * (parts - i)) / parts, (sVert._y * i + eVert._y * (parts - i)) / parts)
                for i in range(1, parts)]
            relayList.extend(sli)


        for i in range(1, len(MSTList)):
            cVert = MSTList[i]
            i_to_p = cVert.getDistance(cVert.Prt)
            # print(i_to_p)
            if i_to_p < 2 * TAR_R:
                relayList.append(cVert.MidNode(cVert.Prt))
            elif i_to_p > 2 * TAR_R:
                sepline(cVert, cVert.Prt, i_to_p)

        return relayList

__all__ = ['loadFromFile', 'Floatfy', 'Vertex', 'matGraph']


if __name__ == '__main__':

    G = matGraph()
    G.initGraph()
    # G.MSpanTree()
    # for i in range(len(G.vertexList)):
    #     print(G.vertexList[i].Prt)
    # pprint(G.AdjMatrix)
    sum = 0
    l = G.MSpanTree()
    for i in range(1, len(l)):
        sum += l[i].getDistance(l[i].Prt)

    distance = sum/(len(l)-1)
    print(distance)
    # print(len(G.STRNP()))
    # for relay in G.STRNP():
    #     print('({:0.1f}, {:0.1f})'.format(relay._x, relay._y))