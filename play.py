#!/usr/bin/env python
# import relevant thingies
import sys
import random
import math
import pygame

from constants import *

import map
import gameObj
import viewport
import playerchar

import mapStorage

#theMap = mapData.makeMap0()
theMap = mapStorage.loadPickle("maps/surface.nzmp")
pc = playerchar.PlayerCharacter(map.MapPos(theMap, [5, 23], 0))

vp = viewport.CameraViewport(pc)
vh = viewport.ViewHolder(1, (0,0), vp, 0)
vh.autoScaleCenter()
layout = viewport.ViewLayout([vh])

while True:
    # determine interact keys available
    f = pc.pos.facing
    tempPos = [pc.pos.xy[0], pc.pos.xy[1]]
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
        obj = theMap.allObjects[tuple(tempPos)]
    except KeyError:
        pass
    if obj != None and obj.interact != None:
        keys = obj.interact.getKeys(thePos.facing)
    else:
        keys = (dict(), dict())

    # event handler (player inputs)
    for event in pygame.event.get():
        # if user wants to quit
        if event.type == QUIT:
            # end the game, close the window
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key in keys[0]: # interaction keys
                keys[0][event.key][1]()
            elif event.key in keys[1]: # hidden interaction keys
                keys[1][event.key][1]()
            else:
                pc.handleKey(event)
        elif event.type == VIDEORESIZE:
            vh.autoScaleCenter()

    DISPLAYSURF.fill((3,3,3))

    vp.update()

    layout.draw()
    pygame.display.update()
    clock.tick(FPS)
