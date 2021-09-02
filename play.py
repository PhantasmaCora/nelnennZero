#!/usr/bin/env python
# import relevant thingies
import sys
import random
import math
import pygame

from constants import *

import map
import viewport

import mapData
theMap = mapData.makeMap0()
thePos = map.MapPos(theMap, [4, 23], 0)

vp = viewport.CameraViewport(thePos)
vh = viewport.ViewHolder(1, (0,0), vp, 0)
vh.autoScaleCenter()
layout = viewport.ViewLayout([vh])

lampFactor = 0

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

    f = random.random() / 2
    lampFactor += f ** 3
    lampScale = 0.05 * math.sin(lampFactor) + 1

    layout.draw(lampScale)
    pygame.display.update()
    clock.tick(FPS)
