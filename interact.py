#!/usr/bin/env python
import sys
import math
import copy

from constants import *

class Interactor(object):
    def __init__(self, interactions):
        self.interactions = {0:[], 1:[], 2:[], 3:[]}
        for inter in interactions:
            inter.core = self
            if inter.facing == -1:
                for n in range(4):
                    self.interactions[n].append(inter)
            else:
                self.interactions[inter.facing].append(inter)

        self.obj = None
        self.pos = None
        self.stateVars = dict()

    def setObjectAssoc(self, obj):
        self.obj = obj
        self.pos = self.obj.pos

    def getText(self, facing):
        ls = []
        for inter in self.interactions[facing]:
            tx = inter.getText()
            if tx != None and tx != "":
                ls.append(tx)
        return ls

    def getKeys(self, facing):
        kd = dict()
        hkd = dict()
        for inter in self.interactions[facing]:
            tkd = inter.getKeys()
            for key in tkd:
                if tkd[key][0] == "":
                    hkd[key] = tkd[key]
                else:
                    kd[key] = tkd[key]
        return (kd, hkd)


class Interaction(object):
    def __init__(self, facing):
        self.facing = facing
        self.core = None

    def getText(self):
        return ""

    def getKeys(self):
        return dict() # tuple: (name, function)
