#!/usr/bin/env python
import sys
import math
import copy

from constants import *

class Interactor(object):
    def __init__(self, text = "", functions = dict()):
        self.text = text
        self.keys = functions
        for key in self.keys:
            self.keys[key].setCore(self)
        self.obj = None

    def setObj(self, obj):
        self.obj = obj

    def getText(self):
        return self.text

    def fire(self, player, key):
        try:
            self.keys[key].fire(player)
        except KeyError:
            pass

class InteractFunction(object):
    def __init__(self):
        self.core = None

    def setCore(self, core):
        self.core = core

    def fire(self, player):
        pass

class MultiFunction(InteractFunction):
    def __init__(self, fns):
        InteractFunction.__init__(self)
        self.functions = fns

    def fire(self, player):
        for fn in self.functions:
            fn.fire(player)

class WallRemoveFn(InteractFunction):
    def __init__(self, wall):
        InteractFunction.__init__(self)
        self.wall = wall

    def fire(self, player):
        pos = self.wall.pos
        pos.map.removeWall(self.wall)

class TeleportFn(InteractFunction):
    def __init__(self, mapname, pos, facing):
        InteractFunction.__init__(self)
        self.mapname = mapname
        self.pos = pos
        self.facing = facing

    def fire(self, player):
        if self.mapname = player.pos.map.name:
            player.pos = map.MapPos(player.pos.map, self.pos, self.facing)
