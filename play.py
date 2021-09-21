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

import mapStorage

#theMap = mapData.makeMap0()
theMap = mapStorage.loadPickle("maps/surface.nzmp")
thePos = map.MapPos(theMap, [4, 23], 0)

vp = viewport.CameraViewport(thePos)
vh = viewport.ViewHolder(1, (0,0), vp, 0)
vh.autoScaleCenter()
layout = viewport.ViewLayout([vh])

while True:
    # determine interact keys available
    f = thePos.facing
    tempPos = [entityPos.xy[0], entityPos.xy[1]]
    if f == 0:
        tempPos[1] -= 1
    elif f == 1:
        tempPos[0] += 1
    elif f == 2:
        tempPos[1] += 1
    elif f == 3:
        tempPos[0] -= 1

    obj = theMap.objects(tuple(tempPos))
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
            elif event.key == K_RIGHT: # basic movement keys
                thePos.facing += 1
                if thePos.facing > 3:
                    thePos.facing -= 4
            elif event.key == K_LEFT:
                thePos.facing -= 1
                if thePos.facing < 0:
                    thePos.facing += 4
            elif event.key == K_UP:
                result = thePos.map.attemptMove(thePos)
                thePos = result[0]
                #print(str(thePos.xy))
                vp.mapPos = thePos
        elif event.type == VIDEORESIZE:
            vh.autoScaleCenter()

    DISPLAYSURF.fill((0,0,0))

    vp.update()

    layout.draw()
    pygame.display.update()
    clock.tick(FPS)
