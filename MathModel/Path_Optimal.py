#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

# from models import Node
import math


ALLOW_TIME = 5.2
VIC = 60

Recure_Pos = [['S1', 3.82, 9.626, 2.55],
              ['S2', 22.92, 100.084, 7.64],
              ['S3', 72.58, 103.904, 13.752],
              ['S4', 87.860, 81.748, 11.69],
              ['S5', 67.232, 84.804, 1.99],
              ['S6', 51.188, 66.468, 8.48],
              ['S7', 39.728, 71.816, 3.056],
              ['S8', 29.032, 67.996, 5.09],
              ['S9', 15.280, 51.188, 9.932],
              ['S10', 72.580, 58.828, 5.32],
              ['S11', 65.704, 55.772, 1.27],
              ['S12', 35.908, 32.088, 1.73]]

class Node:

    def __init__(self, name, x, y, delay=0):
        self.name = name
        self.x = x
        self.y = y
        self.delay = delay
        self.connections = {}

    def getDistance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def addConnection(self, other):
        self.connections[other] = self.getDistance(other)

    def delConnection(self, other):
        del self.connections[other]

    def costTimeTo(self, other):
        return self.getDistance(other)/VIC

    def setDelay(self, ndelay):
        self.delay = ndelay

    def getMinConnect(self):
        if len(self.connections) == 1:
            return tuple(*self.connections.items())
        elif not self.connections:
            return None

        return min(*self.connections.items(), key=lambda x: x[-1])

    def __str__(self):
        return 'Node{}'.format(self.name)



class DoublePoleGraph:
    _pole1 = Node('P1', 110, 0)
    _pole2 = Node('P2', 110, 55)

    def __init__(self):
        self.verList = []
        self.avaliable = [15, 15]

    def addVertex(self, newVertex):

        self._pole2.addConnection(newVertex)
        self._pole1.addConnection(newVertex)
        for vertex in self.verList:
            newVertex.addConnection(vertex)
            vertex.addConnection(newVertex)

        self.verList.append(newVertex)

    def Transverse(self, alwtime):
        PathList = []
        if self.avaliable == [0, 0]:
            return None

        else:
            if self.avaliable[0] > 0 and self.avaliable[1] > 0:
                # print(*self._pole1.connections)
                # print('-----------------------------------')
                # print(*self._pole2.connections)
                check = self._pole1.getMinConnect()[1] < self._pole2.getMinConnect()[1]
            else:
                check = True if self.avaliable[0] > 0 else False
            if check:
                self.avaliable[0] -= 1
                start, curr = self._pole1, self._pole1.getMinConnect()[0]
            else:
                self.avaliable[1] -= 1
                start, curr = self._pole2, self._pole2.getMinConnect()[0]

            PathList.extend([start, curr])

            currentTime = start.costTimeTo(curr)
            Reach = True
            while Reach and len(self.verList) > 1:
                closest = curr.getMinConnect()[0]
                backTime = currentTime + curr.delay + start.costTimeTo(curr)
                nextTime = currentTime + curr.delay + curr.costTimeTo(closest) + start.costTimeTo(closest)
                if nextTime <= alwtime:
                    # print(curr)
                    # print('--------------------')
                    # print(*self.verList)
                    self.verList.remove(curr)
                    self._pole1.delConnection(curr)
                    self._pole2.delConnection(curr)
                    for vert in self.verList:
                        vert.delConnection(curr)

                    currentTime += (curr.delay + curr.costTimeTo(closest))
                    curr = closest
                    PathList.append(curr)
                else:
                    Reach = False
                    if backTime <= alwtime:
                        self.verList.remove(curr)
                        self._pole1.delConnection(curr)
                        self._pole2.delConnection(curr)
                        for vert in self.verList:
                            vert.delConnection(curr)
                        curr = closest

                    else:
                        remain = backTime - alwtime
                        backTime = alwtime
                        curr.setDelay(remain)
            # else:
            #     if not Reach:
            #         return PathList, backTime
            #     else:
            if len(self.verList) == 1:
                    backTime = currentTime + curr.delay + start.costTimeTo(curr)
                    if backTime < alwtime:
                        self.verList.remove(curr)
                        self._pole1.delConnection(curr)
                        self._pole2.delConnection(curr)

                        # return PathList, backTime
                    else:
                        remain = backTime - alwtime
                        backTime = alwtime
                        curr.setDelay(remain)

            return PathList, backTime



DG = DoublePoleGraph()

for item in Recure_Pos:
    DG.addVertex(Node(*item))

while len(DG.verList) >= 1:
    # delays = [(vert.name, vert.delay) for vert in DG.verList]
    path, time = DG.Transverse(ALLOW_TIME)
    # print([item.name for item in DG._pole1.connections.keys()])
    # print(delays)
    print(*path, time)









