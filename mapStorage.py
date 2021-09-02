import sys
import math
import pickle
import os

import map
import mapData

class NelMapHolder(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size

        self.floors = [[None for n in range(size[0])] for n in range(size[1])]
        self.ceils = [[None for n in range(size[0])] for n in range(size[1])]
        self.walls = dict()
        self.plans = None

def storeMap(map):
    mh = NelMapHolder(map.name, map.size)

    # store floors
    floorPlans = []
    for x, col in enumerate(map.floors):
        for y, floor in enumerate(col):
            if floor != None:
                thePlan = floor.toPlan()
                for n, lsPlan in enumerate(floorPlans):
                    if lsPlan == thePlan:
                        mh.floors[x][y] = n
                        break
                else:
                    mh.floors[x][y] = len(floorPlans)
                    floorPlans.append(thePlan)

    # store ceilings
    ceilPlans = []
    for x, col in enumerate(map.ceils):
        for y, ceil in enumerate(col):
            if ceil != None:
                thePlan = floor.toPlan()
                for n, lsPlan in enumerate(ceilPlans):
                    if lsPlan == thePlan:
                        mh.ceils[x][y] = n
                        break
                else:
                    mh.ceils[x][y] = len(ceilPlans)
                    ceilPlans.append(thePlan)

    # store walls
    wallPlans = []
    for key in map.walls:
        for wall in map.walls[key]:
            thePlan = wall.toPlan()
            for n, lsPlan in enumerate(wallPlans):
                if lsPlan == thePlan:
                    mh.walls[(wall.pos.xy[0], wall.pos.xy[1], wall.pos.facing)] = n
                    break
            else:
                mh.walls[(wall.pos.xy[0], wall.pos.xy[1], wall.pos.facing)] = len(wallPlans)
                wallPlans.append(thePlan)

    mh.plans = (floorPlans, ceilPlans, wallPlans)

    return mh

def unstoreMap(mh):
    theMap = map.Map(mh.size, mh.name)

    floorLs = []
    for x, col in enumerate(mh.floors):
        for y, floor in enumerate(col):
            if floor != None:
                floorLs.append(map.Horizontal.fromPlan(map.MapPos(theMap, (x,y), 0), mh.plans[0][floor]))

    theMap.setFloors(floorLs)

    ceilLs = []
    for x, col in enumerate(mh.ceils):
        for y, ceil in enumerate(col):
            if ceil != None:
                ceilLs.append(map.Horizontal.fromPlan(map.MapPos(theMap, (x,y), 0), mh.plans[1][ceil]))

    theMap.setCeils(ceilLs)

    wallLs = []
    for key in mh.walls:
        pos = map.MapPos(theMap, (key[0], key[1]), key[2])
        wallLs.append(map.Wall.fromPlan(pos, mh.plans[2][mh.walls[key]]))

    theMap.addWalls(wallLs)

    return theMap
