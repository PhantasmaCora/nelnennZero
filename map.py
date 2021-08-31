#!/usr/bin/env python
import sys
import math
import pygame
import copy

from constants import *

import transform

class MapPos(object):
    def __init__(self, map, pos, facing):
        self.map = map
        self.xy = pos
        self.facing = facing

class Wall(object):
    def __init__(self, image, pos, viewOffFacing = True, passable = False):
        self.image = image
        self.pos = pos
        self.passable = passable
        self.vof = viewOffFacing

    def getView(self, camPos):
        if self.pos.facing != camPos.facing and not self.vof:
            empty = pygame.Surface((1,1))
            empty.set_colorkey((0,0,0))
            return (empty, 10)

        row = 0
        col = 0
        if camPos.facing == 0:
            row = camPos.xy[1] - self.pos.xy[1] - 1
            col = self.pos.xy[0] - camPos.xy[0] + 1
        elif camPos.facing == 1:
            row = self.pos.xy[0] - camPos.xy[0] - 1
            col = self.pos.xy[1] - camPos.xy[1] + 1
        elif camPos.facing == 2:
            row = self.pos.xy[1] - camPos.xy[1] - 1
            col = camPos.xy[0] - self.pos.xy[0] + 1
        elif camPos.facing == 3:
            row = camPos.xy[0] - self.pos.xy[0] - 1
            col = camPos.xy[1] - self.pos.xy[1] + 1

        level = row
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
            level -= 0.25
            if col == 1 or col == 2:
                level -= 0.5
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
            level -= 0.25
            if col == 1 or col == 2:
                level -= 0.5

        if c0 < 0 or c0 > 3 or c1 < 0 or c1 > 3 or r0 < 0 or r0 > 3 or r1 < 0 or r1 > 3:
            empty = pygame.Surface((1,1))
            empty.set_colorkey((0,0,0))
            return (empty, 10)

        # print(str((r0,c0)) + " " + str((r1,c1)))

        result = transform.wall_transform(self.image, (cRows[r0], cRows[r1], fRows[r0], fRows[r1]), (xCols[r0][c0], xCols[r1][c1]))
        result.set_colorkey((0,0,0))
        return (result, level)

class Floor(object):
    def __init__(self, image, pos, rotate = False, passable = True):
        self.image = image
        self.pos = pos
        self.passable = passable
        self.rotate = rotate

    def getView(self, camPos):
        row = 0
        col = 0
        if camPos.facing == 0:
            row = camPos.xy[1] - self.pos.xy[1] - 1
            col = self.pos.xy[0] - camPos.xy[0] + 1
        elif camPos.facing == 1:
            row = self.pos.xy[0] - camPos.xy[0] - 1
            col = self.pos.xy[1] - camPos.xy[1] + 1
        elif camPos.facing == 2:
            row = self.pos.xy[1] - camPos.xy[1] - 1
            col = camPos.xy[0] - self.pos.xy[0] + 1
        elif camPos.facing == 3:
            row = camPos.xy[0] - self.pos.xy[0] - 1
            col = camPos.xy[1] - self.pos.xy[1] + 1

        img = self.image
        if self.rotate:
            angle = self.pos.facing - camPos.facing
            angle *= -90
            img = pygame.transform.rotate(self.image, angle)
        result = transform.floor_transform(img, (xCols[row + 1][col], xCols[row + 1][col + 1], xCols[row][col], xCols[row][col + 1]), (fRows[row + 1], fRows[row]))
        result.set_colorkey((0,0,0))
        return result

class Ceiling(object):
    def __init__(self, image, pos, rotate = False, passable = True):
        self.image = image
        self.pos = pos
        self.passable = passable
        self.rotate = rotate

    def getView(self, camPos):
        row = 0
        col = 0
        if camPos.facing == 0:
            row = camPos.xy[1] - self.pos.xy[1] - 1
            col = self.pos.xy[0] - camPos.xy[0] + 1
        elif camPos.facing == 1:
            row = self.pos.xy[0] - camPos.xy[0] - 1
            col = self.pos.xy[1] - camPos.xy[1] + 1
        elif camPos.facing == 2:
            row = self.pos.xy[1] - camPos.xy[1] - 1
            col = camPos.xy[0] - self.pos.xy[0] + 1
        elif camPos.facing == 3:
            row = camPos.xy[0] - self.pos.xy[0] - 1
            col = camPos.xy[1] - self.pos.xy[1] + 1

        img = self.image
        if self.rotate:
            angle = self.pos.facing - camPos.facing
            angle *= -90
            img = pygame.transform.rotate(self.image, angle)
        result = transform.floor_transform(img, (xCols[row + 1][col], xCols[row + 1][col + 1], xCols[row][col], xCols[row][col + 1]), (cRows[row], cRows[row + 1]))
        result.set_colorkey((0,0,0))
        return result

class Map(object):
    def __init__(self, size):
        self.floors = [[None for n in range(size[0])] for n in range(size[1])]
        self.ceils = [[None for n in range(size[0])] for n in range(size[1])]
        self.walls = dict()

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

    def setCeiling(self, ceil):
        pos = ceil.pos
        self.ceils[pos.xy[0]][pos.xy[1]] = ceil

    def setCeilings(self, ceilList):
        for f in ceilList:
            self.setCeiling(f)

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

        return (newPos, "succeed")
