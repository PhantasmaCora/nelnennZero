#!/usr/bin/env python
import sys
import math
import copy

import pygame
from constants import *
from map import MapPos
import transform

class GameObject(object):
    def __init__(self, pos, static = True, interact = None, panes = [], passable = True):
        self.pos = pos
        self.static = static
        self.interact = interact
        self.panes = panes
        self.passable = passable
        for pane in self.panes:
            pane.setObjectAssoc(self)

    @classmethod
    def foursider(cls, pos, panePlans, static = True, interact = None, passable = True):
        panes = []
        for pln in panePlans:
            panes.append(ObjectPane.fromPlan(facing = -1, plan = pln))
        return cls(pos, static, interact, panes, passable)

    @classmethod
    def fromPlan(cls, pos, plan, panePlans):
        panesLs = []
        #print(str(plan["panePlanIds"]))
        for tup in plan["panePlanIds"]:
            #print("made pane")
            panesLs.append(ObjectPane.fromPlan(tup[1], panePlans[tup[0]]))
        try:
            plan.pop("panePlanIds")
        except KeyError:
            pass
        return cls(pos, panes = panesLs, **plan)

    def toPlan(self, panePlans):
        panesLs = []
        plan = dict()
        for pane in self.panes:
            thePlan = pane.toPlan()
            for n, lsPlan in enumerate(panePlans):
                if lsPlan == thePlan:
                    panesLs.append((n, pane.facing))
                    break
            else:
                panesLs.append((len(panePlans), pane.facing))
                panePlans.append(thePlan)
        #print(str(panesLs))
        plan["panePlanIds"] = panesLs
        # convert interaction to plan once they exist
        plan["panePlanIds"] = panesLs
        plan["static"] = self.static
        plan["passable"] = self.passable
        return (plan, panePlans)

class ObjectPane(object):
    def __init__(self, facing = 0, imageName = "textures/errorTile.png", viewOffFacing = True, shiftPercentage = 1):
        self.facing = facing
        self.imageName = imageName
        self.image = pygame.image.load(self.imageName)
        self.image.convert_alpha()
        self.vof = viewOffFacing
        self.perc = shiftPercentage

        self.obj = None
        self.pos = None

    def setObjectAssoc(self, obj):
        self.obj = obj
        self.pos = self.obj.pos

    # from an obj plan dict
    @classmethod
    def fromPlan(cls, facing, plan):
        #print("created pane")
        return cls(facing, **plan)

    def toPlan(self):
        plan = dict()
        plan["imageName"] = self.imageName
        plan["viewOffFacing"] = self.vof
        plan["shiftPercentage"] = self.perc
        return plan

    def getView(self, camPos):
        if self.facing != -1 and self.facing != camPos.facing and not self.vof:
            empty = pygame.Surface((1,1))
            empty.set_colorkey((0,0,0))
            return (empty, 10)

        row = 0
        col = 0
        if camPos.facing == 0:
            row = camPos.xy[1] - self.pos.xy[1]
            col = self.pos.xy[0] - camPos.xy[0] + 1
        elif camPos.facing == 1:
            row = self.pos.xy[0] - camPos.xy[0]
            col = self.pos.xy[1] - camPos.xy[1] + 1
        elif camPos.facing == 2:
            row = self.pos.xy[1] - camPos.xy[1]
            col = camPos.xy[0] - self.pos.xy[0] + 1
        elif camPos.facing == 3:
            row = camPos.xy[0] - self.pos.xy[0]
            col = camPos.xy[1] - self.pos.xy[1] + 1

        level = -row
        angle = camPos.facing - self.facing
        if self.facing == -1:
            angle = 0
        angle = angle % 4

        rInter = 1
        cInter = 1

        if angle == 0:
            r0 = row
            c0 = col
            r1 = row
            c1 = col + 1
            rInter = self.perc
            level += self.perc - 1
        elif angle == 1:
            if col < 1:
                r0 = row
                c0 = col + 1
                r1 = row + 1
                c1 = col + 1
            else:
                r1 = row
                c1 = col + 1
                r0 = row + 1
                c0 = col + 1
            cInter = self.perc
            level -= 0.1
            if col == 1 or col == 2:
                level -= 0.1
        elif angle == 3:
            if col < 2:
                r0 = row
                c0 = col
                r1 = row + 1
                c1 = col
            else:
                r1 = row
                c1 = col
                r0 = row + 1
                c0 = col
            cInter = self.perc
            level -= 0.1
            if col == 1 or col == 2:
                level -= 0.1

        if angle == 2 or c0 < 0 or c0 > 3 or c1 < 0 or c1 > 3 or r0 < 0 or r0 > 4 or r1 < 0 or r1 > 4 or (r0 < 1 and r1 < 1) or ((r0 > 3 or r1 > 3) and rInter < 1):
            empty = pygame.Surface((1,1))
            empty.set_colorkey((0,0,0))
            return (empty, 10)

        # print(str((r0,c0)) + " " + str((r1,c1)))

        if rInter < 1:
            a = rInter * cRows[r0] + (1 - rInter) * cRows[r0 + 1]
            b = rInter * cRows[r1] + (1 - rInter) * cRows[r1 + 1]
            c = rInter * fRows[r0] + (1 - rInter) * fRows[r0 + 1]
            d = rInter * fRows[r1] + (1 - rInter) * fRows[r1 + 1]
        else:
            a = cRows[r0]
            b = cRows[r1]
            c = fRows[r0]
            d = fRows[r1]

        if angle == 0:
            ls = round(rInter * xCols[r0][c0] + (1 - rInter) * xCols[r0 + 1][c0])
            rs = round(rInter * xCols[r1][c1] + (1 - rInter) * xCols[r1 + 1][c1])
        elif angle == 1 and cInter < 1:
            ls = round(cInter * xCols[r0][c0] + (1 - cInter) * xCols[r0][c0 - 1])
            rs = round(cInter * xCols[r1][c1] + (1 - cInter) * xCols[r1][c1 - 1])
        elif angle == 3 and cInter < 1:
            ls = round(cInter * xCols[r0][c0] + (1 - cInter) * xCols[r0][c0 + 1])
            rs = round(cInter * xCols[r1][c1] + (1 - cInter) * xCols[r1][c1 + 1])
        else:
            ls = xCols[r0][c0]
            rs = xCols[r1][c1]

        result = transform.wall_transform(self.image, (a, b, c, d), (ls, rs))
        result.set_colorkey((0,0,0))
        return (result, level)
