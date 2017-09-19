#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''

import math

LENGTH = 111.0
WIDTH = 106.0
SINWIDTH = 0.6
VIC = 60
TIME = 3


class Path:
    def __init__(self):
        self.startpos = (SINWIDTH, SINWIDTH)
        self.loops = 44
        self.LL1 = LENGTH - SINWIDTH * 2
        self.LL2 = self.LL1 - SINWIDTH * 2

        self.WW2 = SINWIDTH * 2
        self.WW1 = self.WW2 * (2 * self.loops - 1)
        self.looplength = (self.WW2 + self.LL2) * 2


    def verify(self, x, y):
        step, rem = divmod(x-SINWIDTH, self.WW2*2)
        if step < 0 or step >= self.loops:
            return False
        elif step == self.loops -1:
            if rem - self.WW2 > 1e-6:
                return False
            elif abs(rem - self.WW2) < 1e-6:
                return (y > SINWIDTH-1e-6) and (y < LENGTH - SINWIDTH + 1e-6)

            elif rem < 1e-6:
                return (y > SINWIDTH*3 - 1e-6) and (y < LENGTH - SINWIDTH + 1e-6)

            else:
                return abs(y - SINWIDTH*3) < 1e-6 or abs(y - LENGTH + SINWIDTH) < 1e-6
        elif step == 0:
            if rem < 1e-6:
                return (y > SINWIDTH-1e-6) and (y < LENGTH - SINWIDTH + 1e-6)
            elif rem < SINWIDTH - 1e-6:
                return abs(y - SINWIDTH) < 1e-6 or abs(y - LENGTH + SINWIDTH) < 1e-6
            elif abs(rem - self.WW2) < 1e-6:
                return ((y > SINWIDTH-1e-6) and (y < LENGTH - SINWIDTH + 1e-6)) or abs(y - SINWIDTH) < 1e-6
            else:
                return abs(y - SINWIDTH*3) < 1e-6 or abs(y - SINWIDTH) <1e-6

        else:
            if rem < 1e-6:
                return (y > SINWIDTH*3 - 1e-6) and (y < LENGTH - SINWIDTH + 1e-6)
            elif rem < SINWIDTH - 1e-6:
                return abs(y - SINWIDTH) < 1e-6 or abs(y - LENGTH + SINWIDTH) < 1e-6
            elif abs(rem - self.WW2) < 1e-6:
                return ((y > SINWIDTH-1e-6) and (y < LENGTH - SINWIDTH + 1e-6)) or abs(y - SINWIDTH) < 1e-6
            else:
                return abs(y - SINWIDTH*3) < 1e-6 or abs(y - SINWIDTH) <1e-6



    def TranstoL(self, x, y):
        if self.verify(x, y):
            if abs(y - SINWIDTH) < 1e-6:
                return self.getWholeLength() - x + SINWIDTH
            elif abs(x - SINWIDTH - self.WW1) < 1e-6:
                return self.getWholeLength() - self.WW1 - y + SINWIDTH
            elif x < 1e-6:
                return y - SINWIDTH
            else:
                step, ram = divmod(x-SINWIDTH, 2*SINWIDTH)
                pass


    def TranstoCoor(self, L):
        if L < self.WW2:
            return 0, L
        elif L > self.getWholeLength():
            return self.TranstoCoor(L - self.getWholeLength())
        elif L + self.WW1 > self.getWholeLength():
            x = self.getWholeLength() - L
            return x, 0
        else:
            step, ram = divmod(L-self.WW2, self.looplength)
            if step == 44 and ram > self.looplength - self.WW2:
                return self.WW1, self.looplength-ram
            else:
                if ram < self.LL2:
                    return step*self.WW2*2, ram+self.WW2
                elif ram < self.LL2+self.WW2:
                    return step*self.WW2*2 + ram - self.LL2, self.LL2+self.WW2
                elif ram < self.looplength - self.WW2:
                    return step*self.WW2*2 + self.WW2, self.looplength-self.WW2-ram+self.WW2
                else:
                    return (step+1)*self.WW2*2 + ram -self.looplength, self.WW2


    def getWholeLength(self):
        return self.WW1 + self.loops*(self.WW2*2 + self.LL2*2) + self.WW2

    def getLineLength(self, L):
        gap_x, gap_y = self.TranstoCoor(L)
        return math.sqrt(gap_x**2 + gap_y**2)


class uav:
    def __init__(self, name):
        self.name = name
        self.vic = VIC
        self.startT = 0

    def setStartTime(self, time):
        self.startT = time

    def getStartTime(self):
        return self.startT

    def getFTime(self, L):
        return L/self.vic

    def __str__(self):
        return 'uav{}: startT{}'.format(self.name, self.startT)



class UAVs:

    def __init__(self):
        self.uavList = []
        self.num = 0

    def addUAV(self, p):
        self.num += 1
        newUav = uav(self.num)
        self.uavList.append(newUav)
        if self.num > 1:
            preUav = self.uavList[self.num-2]
            inittime = preUav.startT + TIME
            pL = preUav.vic * preUav.startT
            pLL = p.getLineLength(pL)
            # t0, t1 = 0, newUav.getFTime(LL)
            # while t0/t1 < 0.95:
            #     t0 = (t0 + t1)/2
            #     L = VIC * (inittime + t0)
            #     LL = p.getLineLength(L)
            #     t1 = newUav.getFTime(LL)
            # newUav.setStartTime(inittime + t0)
            tp = newUav.getFTime(pLL)
            nLL = p.getLineLength(VIC*inittime)
            tn = newUav.getFTime(nLL)
            delta_t = 0
            while abs(tn - tp) > 0.005 :
                # print(tp, tn)
                delta_t = (tn - tp)/2
                tp += delta_t
                nLL = p.getLineLength(VIC*(inittime + delta_t))
                tn = newUav.getFTime(nLL)
            g_x, g_y = p.TranstoCoor(VIC*(inittime+delta_t))
            print(round(g_x+SINWIDTH, 3), round(g_y+SINWIDTH, 3))
            newUav.setStartTime(inittime + delta_t)





p = Path()
# L = TIME * VIC
# u1 = uav('1')
# t = u1.getTime(L)
# for i in range(10):
#     LL = p.getLineLength(L)
#     t1 = L/VIC -TIME
#     t2 = u1.getTime(LL)
#     delta = (t2 - t1)/2
#     L += delta * VIC
#     print(t1, t2)
print(p.getWholeLength())
UAVqun = UAVs()
for i in range(55):
    UAVqun.addUAV(p)
for item in UAVqun.uavList:
    print(item)