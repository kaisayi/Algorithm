#! /usr/bin/env/python
# -*- coding:utf-8 -*-
'''
@version: python3.5
@author: Liyi
'''
from Clulstering_by_Distance import *
import random, copy
VIC = 100
Dset = DistriDot()
Dset.CreteDots()
Dset.InitCenter()
cluster = Dset.ClusterbyNum()
Dset.ClassifybyDistance()

DotList = [(52.2, 120.4, 0.046931194),
           (67.8, 116.5, 0.054151378),
           (91.2, 124.3, 0.058663993)]

NodeList = [Node(*item) for item in DotList]
for vert in NodeList:
    distance, closetVert = min((vert.getDistance(center) for center in cluster),
                               key=lambda x: x[0])

    cluster[closetVert].add(vert)

# for key, value in cluster.items():
#         for node in value:
#             print(node.x, node.y)
#         print('**********************************************')


# generate a person

class Person:

    def __init__(self, gene):
        self.gene = list(gene)
        random.shuffle(self.gene)
        self.cost = 0
        self.fitness = 0
        self.p = 0
        self.SetInitValue()

    def SetInitValue(self):
        wholeDelay = sum(node.delay for node in self.gene)
        self.cost = wholeDelay + sum(self.gene[i].getDistance(self.gene[i+1])[0]/100
                                     for i in range(len(self.gene)-1))

        self.fitness = 1/self.cost

    def Cross(self, other):
        gene = [0] * len(self.gene)
        not_used = copy.copy(self.gene)
        for i in range(len(self.gene)):
            if self.gene[i] in not_used and other.gene[i] in not_used:
                gene[i] = self.gene[i] if random.random()<0.5 else other.gene[i]
            elif self.gene[i] in not_used:
                gene[i] = self.gene[i]
            elif self.gene[i] in not_used:
                gene[i] = self.gene[i]
            else:
                gene[i] = not_used[random.randint(0, len(not_used)-1)]
            not_used.remove(gene[i])
        return gene

    def Mutate(self):
        gene = copy.copy(self.gene)
        for i in range(random.randint(0, len(self.gene)//2)):
            x = random.randint(0, len(self.gene)-1)
            y = random.randint(0, len(self.gene)-1)
            gene[x], gene[y] = gene[y], gene[x]
        return gene



    def __str__(self):
        return '{} fitness={} cost={}'.format(self.gene, self.fitness, self.cost)

    def __lt__(self, other):
        return self.fitness > other.fitness



# create a class People

class People:
    def __init__(self, geneScale):
        self.geneScale = geneScale
        self.size = 10
        self.crossProbalibility = 0.5
        self.mutationProbalility = 0.3
        self.generationCnt = 1000
        # self.mutationScale = self.geneScale // 2
        self.persons = []

    def CreatePersons(self, gene):
        for i in range(self.size):
            self.persons.append(Person(gene))

    def getLiveChance(self):
        total = sum(person.fitness for person in self.persons)
        for person in self.persons:
            person.p = person.fitness/total

    def SelectStronger(self):
        chance = 0
        randChance = random.random()
        for person in self.persons:
            chance += person.p
            if chance >= randChance:
                return person

    def Generate(self):
        for generation in range(self.generationCnt):
            self.getLiveChance()
            if random.random() < self.crossProbalibility:
                pa1 = self.SelectStronger()
                pa2 = self.SelectStronger()
                self.persons.append(Person(pa1.Cross(pa2)))
            if random.random() < self.mutationProbalility:
                mute_person = Person(self.persons[random.randint(0, self.size-1)].Mutate())
                self.persons.append(mute_person)
            sorted(self.persons, key=lambda p: p.fitness)
        return self.persons[0]


if __name__ == '__main__':
    for key, value in cluster.items():
        PP = People(len(value))
        PP.CreatePersons(value)
        Optimal_Path = PP.Generate()
        for node in Optimal_Path.gene:
            print(node.x, node.y)
        print(Optimal_Path.cost)
        print('***********************************')








