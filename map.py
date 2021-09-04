#!/usr/bin/env python
import sys
import math
import copy

from constants import *

import transform

class MapPos(object):
    def __init__(self, map, pos, facing):
        self.map = map
        self.xy = pos
        self.facing = facing

    def __eq__(self, other):
        if not isinstance(other, MapPos):
            return False
        return (self.map == other.map and self.xy[0] == other.xy[0] and self.xy[1] == other.xy[1] and self.facing == other.facing)

class Wall(object):
    def __init__(self, pos, imageName = "textures/errorTile.png", passable = False, seeThrough = False, viewOffFacing = True):
        self.pos = pos
        self.imageName = imageName
        self.image = pygame.image.load(self.imageName)
        self.passable = passable
        self.seeThrough = seeThrough
        self.vof = viewOffFacing

    # config = dict w/ kwargs
    @classmethod
    def make(cls, pos, config):
        return cls(pos, **config)

    # from a wall plan dict
    @classmethod
    def fromPlan(cls, pos, plan):
        return cls.make(pos, plan)

    def toPlan(self):
        plan = dict()
        plan["imageName"] = self.imageName
        plan["passable"] = self.passable
        plan["viewOffFacing"] = self.vof
        plan["seeThrough"] = self.seeThrough
        return plan

    def getView(self, camPos):
        if self.pos.facing != camPos.facing and not self.vof:
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
        angle = camPos.facing - self.pos.facing
        angle = angle % 4

        if angle == 0:
            r0 = row
            c0 = col
            r1 = row
            c1 = col + 1
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
            level -= 0.1
            if col == 1 or col == 2:
                level -= 0.1
        elif angle == 2:
            r0 = row + 1
            c0 = col
            r1 = row + 1
            c1 = col + 1
            level -= 1
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
            level -= 0.1
            if col == 1 or col == 2:
                level -= 0.1

        if c0 < 0 or c0 > 3 or c1 < 0 or c1 > 3 or r0 < 0 or r0 > 4 or r1 < 0 or r1 > 4 or (r0 < 1 and r1 < 1):
            empty = pygame.Surface((1,1))
            empty.set_colorkey((0,0,0))
            return (empty, 10)

        # print(str((r0,c0)) + " " + str((r1,c1)))

        result = transform.wall_transform(self.image, (cRows[r0], cRows[r1], fRows[r0], fRows[r1]), (xCols[r0][c0], xCols[r1][c1]))
        if r0 == 0 and c0 == 1 and not self.seeThrough:
            result.fill((1,1,1), pygame.Rect(0, 0, xCols[0][1], 512))
        if r1 == 0 and c1 == 2 and not self.seeThrough:
            r2 = pygame.Surface((512,512))
            r2.fill((1,1,1))
            r2.blit(result, (0,0))
            result = r2
        result.set_colorkey((0,0,0))
        return (result, level)

class Horizontal(object):
    def __init__(self, pos, imageName = "textures/errorTile.png", passable = True, rotate = False):
        self.pos = pos
        self.imageName = imageName
        self.image = pygame.image.load(self.imageName)

        self.passable = passable
        self.rotate = rotate

    # config = dict w/ kwargs
    @classmethod
    def make(cls, pos, config):
        return cls(pos, **config)

    # from a horizontal plan dict
    @classmethod
    def fromPlan(cls, pos, plan):
        config = copy.copy(plan)
        if "specRotation" in config:
            pos.facing = config["specRotation"]
            config.pop("specRotation")
        if config["type"] == "f":
            config.pop("type")
            return Floor.make(pos, config)
        elif config["type"] == "c":
            config.pop("type")
            return Ceiling.make(pos, config)
        else:
            print("invalid horizontal plan type!!")

    def toPlan(self):
        plan = dict()
        plan["imageName"] = self.imageName
        plan["passable"] = self.passable
        plan["rotate"] = self.rotate
        if plan["rotate"]:
            plan["specRotation"] = self.pos.facing
        if isinstance(self, Floor):
            plan["type"] = "f"
        elif isinstance(self, Ceiling):
            plan["type"] = "c"
        else:
            print("Horizontal object should never be used directly, only through it's subclasses!")
        return plan

    def getView(self, camPos):
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

        img = self.image
        if self.rotate:
            angle = self.pos.facing - camPos.facing
            angle *= -90
            img = pygame.transform.rotate(self.image, angle)
        result = self.properTransform(img, row, col)
        result.set_colorkey((0,0,0))
        return result

    # should never be used
    def properTransform(self, img, row, col):
        print("warning: 'Horizontal' class should never be directly used, only it's subclasses")
        return img

class Floor(Horizontal):
    def properTransform(self, img, row, col):
        #print("transformed")
        return transform.floor_transform(img, (xCols[row + 1][col], xCols[row + 1][col + 1], xCols[row][col], xCols[row][col + 1]), (fRows[row + 1], fRows[row]))

class Ceiling(Horizontal):
    def properTransform(self, img, row, col):
        return transform.floor_transform(img, (xCols[row + 1][col], xCols[row + 1][col + 1], xCols[row][col], xCols[row][col + 1]), (cRows[row], cRows[row + 1]))

class Map(object):
    def __init__(self, size, name):
        self.size = size
        self.floors = [[None for n in range(size[0])] for n in range(size[1])]
        self.ceils = [[None for n in range(size[0])] for n in range(size[1])]
        self.walls = dict()
        self.name = name

        self.allObjects = dict()
        self.staticObjects = dict()
        self.dynamicObjects = dict()

    def setFloor(self, floor):
        pos = floor.pos
        self.floors[pos.xy[0]][pos.xy[1]] = floor

    def setFloors(self, floorList):
        for f in floorList:
            self.setFloor(f)

    def getFloor(self, pos):
        try:
            floor = self.floors[pos[0]][pos[1]]
        except IndexError:
            return None
        return floor

    def setCeil(self, ceil):
        pos = ceil.pos
        self.ceils[pos.xy[0]][pos.xy[1]] = ceil

    def setCeils(self, ceilList):
        for f in ceilList:
            self.setCeil(f)

    def getCeiling(self, pos):
        try:
            ceil = self.ceils[pos[0]][pos[1]]
        except IndexError:
            return None
        return ceil

    def addWall(self, wall):
        location = (wall.pos.xy[0], wall.pos.xy[1])
        try:
            self.walls[location].append(wall)
        except KeyError:
            self.walls[location] = [wall]

    def addWalls(self, wallList):
        for w in wallList:
            self.addWall(w)

    def getWalls(self, pos):
        try:
            return self.walls[pos]
        except KeyError:
            return []

    def addObj(self, obj):
        if not obj.pos.xy in self.allObjects:
            self.allObjects[obj.pos.xy] = obj
            if obj.static:
                self.staticObjects[obj.pos.xy] = obj
            else:
                self.dynamicObjects[obj.pos.xy] = obj
            return True
        else:
            return False

    def addObjs(self, ls):
        for obj in ls:
            self.addObj(obj)

    def attemptMove(self, entityPos):
        f = entityPos.facing
        tempPos = [entityPos.xy[0], entityPos.xy[1]]
        if f == 0:
            tempPos[1] -= 1
        elif f == 1:
            tempPos[0] += 1
        elif f == 2:
            tempPos[1] += 1
        elif f == 3:
            tempPos[0] -= 1

        newPos = MapPos(self, tuple(tempPos), entityPos.facing)

        for wall in self.getWalls(tuple(entityPos.xy)):
            if wall.passable == False and (wall.pos.facing - entityPos.facing) % 4 == 2:
                return (entityPos, "fail")
        for wall in self.getWalls(tuple(newPos.xy)):
            if wall.passable == False and (wall.pos.facing - newPos.facing) % 4 == 0:
                return (entityPos, "fail")
        # if newPos tile not passable return fail
        floor = self.floors[newPos.xy[0]][newPos.xy[1]]
        if floor != None and floor.passable == False:
            return (entityPos, "fail")
        # if newPos contains impassible object return fail
        obj = None
        try:
            obj = self.allObjects[(newPos.xy[0], newPos.xy[1])]
        except KeyError:
            pass
        if obj != None and obj.passable == False:
            return (entityPos, "fail")

        return (newPos, "succeed")
