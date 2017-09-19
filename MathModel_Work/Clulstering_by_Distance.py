#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

from MST import *

import math

class Node:

    def __init__(self, x, y, delay=0):
        self.x = x
        self.y = y
        self.delay = delay

    def getDistance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2), other



class DistriDot:

    def __init__(self):
        self.nodeList = []
        self.TripleCenter = {}

    def CreteDots(self):
        for item in DISK_CENTER:
            self.nodeList.append(Node(*item))


    def InitCenter(self):
        if len(self.nodeList) < 4:
            raise RuntimeError('Can not run the function')
        self.TripleCenter[self.nodeList[0]] = set()
        self.TripleCenter[self.nodeList[1]] = set()
        self.TripleCenter[self.nodeList[2]] = set()

    # put all the datas into the three sets
    def ClassifybyDistance(self):
        if len(self.TripleCenter) < 3:
            raise RuntimeError('The TripleCenter must >= 3')

        for vert in self.nodeList:
            distance, closetVert = min((vert.getDistance(center) for center in self.TripleCenter),
                                       key=lambda x: x[0])

            self.TripleCenter[closetVert].add(vert)

    def ClusterbyNum(self):

        def getCenterPoint(aset):
            center_x = sum(vert.x for vert in aset)/len(aset)
            center_y = sum(vert.y for vert in aset)/len(aset)
            return center_x, center_y


        for i in range(10):
            self.ClassifybyDistance()
            for center in self.TripleCenter:
                if len(self.TripleCenter[center]) < 1:
                    continue
                else:
                    center_x, center_y = getCenterPoint(self.TripleCenter[center])
                    # print(center_x, center_y)
                    del self.TripleCenter[center]
                    self.TripleCenter[Node(center_x, center_y)] = set()
            # print('-********************************************************-')
        return self.TripleCenter



DISK_CENTER=[(30.0, 90.6, 0.043997994),
             (30.0, 99.4, 0.037050943),
             (44.5, 31.0, 0.119139388),
             (44.5, 36.0, 0.058663993),
             (43.35, 76.95, 0.117404246),
             (44.5, 86.7, 0.043997994),
             (47.8, 25.8, 0.039109328),
             (51.1, 38.8, 0.046931194),
             (50.0, 71.7, 0.035198396),
             (50.0, 78.9, 0.035198396),
             (51.1, 88.9, 0.041409877),
             (55.5, 12.9, 0.050283422),
             (52.3, 16.8, 0.035198396),
             (55.1, 22.0, 0.046931194),
             (52.8, 66.6, 0.090717431),
             (55.6, 71.2, 0.046931194),
             (53.95, 79.3, 0.035198396),
             #(52.2, 120.4, 0.046931194),
             (58.35, 25.85, 0.144626291),
             (58.3, 36.85, 0.091904071),
             (61.2, 45.3, 0.050283422),
             (60.0, 53.0, 0.041409877),
             (57.8, 89.7, 0.085997418),
             (58.9, 92.7, 0.043997994),
             (64.9, 39.45, 0.035198396),
             (62.2, 82.9, 0.058663993),
             (64.15, 93.4, 0.11387003),
             (67.8, 31.0, 0.037050943),
             (67.0, 38.8, 0.039109328),
             (69.5, 44.0, 0.091692487),
             (71.1, 52.9, 0.050283422),
             #(67.8, 116.5, 0.054151378),
             (74.5, 15.5, 0.050283422),
             (72.3, 19.4, 0.058663993),
             (73.3, 27.1, 0.154795353),
             (75.0, 27.1, 0.070396791),
             (75.25, 35.4, 0.085726076),
             (74.5, 46.6, 0.063997083),
             (72.3, 64.7, 0.058663993),
             (76.15, 90.1, 0.039109328),
             (81.1, 22.0, 0.054151378),
             (80.1, 28.4, 0.037050943),
             (78.95, 41.5, 0.121450434),
             (80.0, 47.7, 0.150507869),
             (77.9, 51.7, 0.050283422),
             (78.9, 93.2, 0.037050943),
             (84.4, 25.8, 0.046931194),
             (82.2, 44.4, 0.050283422),
             (84.87, 57.77, 0.158785453),
             (85.6, 60.8, 0.070396791),
             (82.3, 66.65, 0.118263582),
             (85.6, 71.2, 0.058663993),
             (83.4, 90.4, 0.043997994),
             (91.2, 94.3, 0.039109328)]
             #(91.2, 124.3, 0.058663993)]


__all__ = ['Node', 'DistriDot', 'DISK_CENTER']

if __name__ == '__main__':
    Dset = DistriDot()
    Dset.CreteDots()
    Dset.InitCenter()
    cluster = Dset.ClusterbyNum()
    Dset.ClassifybyDistance()

    # for key, value in cluster.items():
    #     for node in value:
    #         print(node.x, node.y)
    #     print('**********************************************')






























