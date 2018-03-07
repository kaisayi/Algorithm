#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''


SCAN_WIDTH = 5.0

import math
from MST import *
from pprint import pprint

G = matGraph()
G.initGraph()
RIGHTBOUND, LEFTBOUND = G.getXRange()
# RIGHTBOUND -= SCAN_WIDTH
# LEFTBOUND += SCAN_WIDTH
RAWDIVIDE = math.ceil((LEFTBOUND - RIGHTBOUND)/SCAN_WIDTH)

class scanStrip:

    def __init__(self, rgtBound):
        self.halfWidth = SCAN_WIDTH/2
        self.rgtBound = rgtBound
        self.verList = []

    def verify(self, vert):
        return vert._x >= self.rgtBound and vert._x < self.rgtBound + self.halfWidth * 2

    def addVertex(self, vert):
        if self.verify(vert):
            if vert not in self.verList:
                self.verList.append(vert)

    def initVerlist(self):
        for vert in G.vertexList:
            self.addVertex(vert)

    def getMinY(self):
        if len(self.verList) == 1:
            return self.verList[0]
        return min(self.verList, key=lambda v: v._y)

    def isInDisk(self, center, vert):
        return center.getDistance(vert) <= self.halfWidth + 1e-4

    def getMiniCover(self):
        diskList = []
        midLine = self.rgtBound + self.halfWidth
        while self.verList:
            belowVert = self.getMinY()
            self.verList.remove(belowVert)  # delete the mini_y vertex

            bias_x = abs(belowVert._x - midLine)
            bias_y = math.sqrt(self.halfWidth**2 - bias_x**2)
            center_y = belowVert._y + bias_y
            center = Vertex(midLine, center_y)
            diskList.append(center)
            if not self.verList:
                break

            # if vert in disk, remove the vertex
            for vert in self.verList:
                if self.isInDisk(center, vert):
                    self.verList.remove(vert)
            # print(len(self.verList))

        return diskList


def Mutiple(func):

    def decorator(rgtBound):
        L = 10
        diskNum = 100
        minList = []
        for i in range(L):
            rgt = rgtBound - SCAN_WIDTH*i/L
            disks = func(rgt)
            for disk in disks:
                print(disk._x, disk._y)

            print('******************************************************')
            if len(disks) < diskNum:
                minList = disks
                diskNum = len(disks)
        print('The Mini Cover Disk: ')
        with open('disk.txt', 'w+') as f:
            for vert in minList:
                f.write('{}, {}\n'.format(vert._x, vert._y))
                print(vert._x, vert._y)

        print(len(minList))
        return minList
    return decorator





# scanS1 = scanStrip(30.0)
# for vert in G.vertexList:
#     scanS1.addVertex(vert)
# Biun
# print(len(scanS1.verList))
# print(scanS1.getMiniCover())

@Mutiple
def OneLoopCover(rgtBound):
    divided = RAWDIVIDE
    lftbound = rgtBound + divided * SCAN_WIDTH
    while lftbound < LEFTBOUND:
        lftbound += SCAN_WIDTH
        divided += 1
    Disklist = []
    for i in range(divided):
        ScanStp = scanStrip(rgtBound)
        ScanStp.initVerlist()
        Disklist.extend(ScanStp.getMiniCover())
        rgtBound = rgtBound + SCAN_WIDTH

    return Disklist





if __name__ == '__main__':
    disklist = OneLoopCover(RIGHTBOUND)
    diskDic = {}
    for vert in disklist:
        diskDic[(vert._x, vert._y)] = [(v._x, v._y) for v in G.InDiskVertex(vert, SCAN_WIDTH/2)]
    for key, value in diskDic.items():
        if value == []:
            continue
        elif len(value) == 1:
            center_x, center_y = value[0]
            print(center_x, center_y)
        else:
            center_x, center_y = zip(*value)
            print(sum(center_x)/len(center_x), sum(center_y)/len(center_y))








