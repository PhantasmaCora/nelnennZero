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
    # event handler (player inputs)
    for event in pygame.event.get():
        # if user wants to quit
        if event.type == QUIT:
            # end the game, close the window
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            pc.handleKey(event)
        elif event.type == VIDEORESIZE:
            vh.autoScaleCenter()

    DISPLAYSURF.fill((3,3,3))

    vp.update()

    layout.draw()
    pygame.display.update()
    clock.tick(FPS)
