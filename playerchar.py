#!/usr/bin/env python
import sys
import math
import copy

import pygame
from constants import *
from map import MapPos

class PlayerCharacter(object):
    def __init__(self, pos):
        self.pos = pos

    def handleKey(self, event):
        # determine interact keys available
        f = self.pos.facing
        tempPos = [self.pos.xy[0], self.pos.xy[1]]
        if f == 0:
            tempPos[1] -= 1
        elif f == 1:
            tempPos[0] += 1
        elif f == 2:
            tempPos[1] += 1
        elif f == 3:
            tempPos[0] -= 1
        obj = None
        try:
            obj = self.pos.map.allObjects[tuple(tempPos)]
        except KeyError:
            pass
        if obj != None and obj.interact != None:
            keys = obj.interact.getKeys(f.facing)
        else:
            keys = (dict(), dict())

        if event.key in keys[0]: # interaction keys
            keys[0][event.key][1]()
        elif event.key in keys[1]: # hidden interaction keys
            keys[1][event.key][1]()
        elif event.key == K_RIGHT: # basic movement keys
            self.pos.facing += 1
            if self.pos.facing > 3:
                self.pos.facing -= 4
        elif event.key == K_LEFT:
            self.pos.facing -= 1
            if self.pos.facing < 0:
                self.pos.facing += 4
        elif event.key == K_UP:
            result = self.pos.map.attemptMove(self.pos)
            self.pos = result[0]
