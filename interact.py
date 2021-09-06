#!/usr/bin/env python
import sys
import math
import copy

from constants import *

class Interactor(object):
    def __init__(self, interactions):
        self.interactions = {0:[], 1:[], 2:[], 3:[]}
        for inter in interactions:
            if inter.facing == -1:
                for n in range(4):
                    self.interactions[n].append(inter)
            else:
                self.interactions[inter.facing].append(inter)

        self.obj = None
        self.pos = None

    def setObjectAssoc(self, obj):
        self.obj = obj
        self.pos = self.obj.pos

class Interaction(object):
    def __init__(self, facing):
        self.facing = facing
