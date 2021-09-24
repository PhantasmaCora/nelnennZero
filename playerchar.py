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
        if event.key == K_RIGHT: # basic movement keys
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
