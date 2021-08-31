#!/usr/bin/env python
# import relevant thingies
import sys
import random
import math
import pygame

from constants import *

import map
import viewport

theMap = map.Map((24, 24))
thePos = map.MapPos(theMap, [12, 23], 0)

tile = pygame.image.load("textures/floorBrick.png")
grass = pygame.image.load("textures/floorGrass.png")
end = pygame.image.load("textures/floorPathEnd.png")
turn = pygame.image.load("textures/floorPathTurn.png")
straight = pygame.image.load("textures/floorPathLine.png")
f0 = map.Floor(tile, map.MapPos(theMap, (12, 20), 0))
f1 = map.Floor(turn, map.MapPos(theMap, (11, 21), 2), True)
f2 = map.Floor(end, map.MapPos(theMap, (11, 20), 2), True)
f3 = map.Floor(straight, map.MapPos(theMap, (12, 21), 1), True)
f4 = map.Floor(turn, map.MapPos(theMap, (13, 21), 0), True)
f5 = map.Floor(tile, map.MapPos(theMap, (12, 22), 0))
f6 = map.Floor(end, map.MapPos(theMap, (13, 22), 0), True)
f7 = map.Floor(grass, map.MapPos(theMap, (11, 22), 0))
f8 = map.Floor(grass, map.MapPos(theMap, (13, 20), 0))
theMap.setFloors([f0, f1, f2, f3, f4, f5, f6, f7, f8])

wall = pygame.image.load("textures/wallBrick.png")
w0 = map.Wall(wall, map.MapPos(theMap, (12, 20), 2))
theMap.addWalls([w0])

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
                f = thePos.facing
                if f == 0:
                    thePos.xy[1] -= 1
                elif f == 1:
                    thePos.xy[0] += 1
                elif f == 2:
                    thePos.xy[1] += 1
                elif f == 3:
                    thePos.xy[0] -= 1

    DISPLAYSURF.fill((0,0,0))

    f = random.random() / 2
    lampFactor += f ** 3
    lampScale = 0.05 * math.sin(lampFactor) + 1

    layout.draw(lampScale)
    pygame.display.update()
    clock.tick(FPS)
