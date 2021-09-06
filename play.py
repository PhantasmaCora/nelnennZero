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

#wl = map.Wall(map.MapPos(theMap, (4, 17), 0), imageName = "textures/wallBookshelf.png", viewOffFacing = False)
#theMap.addWall(wl)

vp = viewport.CameraViewport(thePos)
vh = viewport.ViewHolder(1, (0,0), vp, 0)
vh.autoScaleCenter()
layout = viewport.ViewLayout([vh])

while True:
    # event handler (player inputs)
    for event in pygame.event.get():
        # if user wants to quit
        if event.type == QUIT:
            # end the game, close the window
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
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
