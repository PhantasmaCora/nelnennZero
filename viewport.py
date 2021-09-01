#!/usr/bin/env python
import sys
import math
import pygame
import copy

from constants import *

class Viewport(object):
    def __init__(self, size):
        self.size = size
        self.rendersurf = pygame.Surface(self.size)
        self.zoom = 1

    def draw(self):
        pass

    def getRenderSurf(self):
        return self.rendersurf

    def toGameSpace(self, coords):
        return Vector(0,0)

class CameraViewport(Viewport):
    def __init__(self, mapPos):
        Viewport.__init__(self, (512, 512))
        self.cached = None
        import map
        self.cachePos = map.MapPos(mapPos.map, (-1,-1), -1)
        self.mapPos = mapPos

    def draw(self, lf):
        self.rendersurf.fill((0,0,0))
        # check whether cached terrain images are still correct
        if self.mapPos == self.cachePos:
            pass
        else:
            self.cachePos = copy.copy(self.mapPos) # mark this as new cache position
            #print("new cache")
            self.cached = self.rendersurf.copy()
            # draw floors and ceilings
            for offset in camZone[self.mapPos.facing]:
                pos = [self.mapPos.xy[0], self.mapPos.xy[1]]
                pos[0] += offset[0]
                pos[1] += offset[1]
                fl = self.mapPos.map.getFloor(pos)
                if fl != None:
                    self.cached.blit(fl.getView(self.mapPos), (0,0))
                cl = self.mapPos.map.getCeiling(pos)
                if cl != None:
                    self.cached.blit(cl.getView(self.mapPos), (0,0))

            # draw walls
            # 1. acquire walls to list
            ls = []
            for offset in camZoneWall[self.mapPos.facing]:
                pos = [self.mapPos.xy[0], self.mapPos.xy[1]]
                pos[0] += offset[0]
                pos[1] += offset[1]
                ls.extend(self.mapPos.map.getWalls(tuple(pos)))
            # 2. acquire images from walls
            ls2 = []
            for wall in ls:
                ls2.append(wall.getView(self.mapPos))
            ls2.sort(key=lambda tup: tup[1]) # sort by z-level, putting furthest away at start of list
            for tup in ls2:
                self.cached.blit(tup[0], (0,0))

        # blit terrain cache to rendering surface
        self.rendersurf.blit(self.cached, (0,0))

        # final step - render lantern darkness
        dark = pygame.transform.smoothscale(lanternImg, (round(640 * lf), round(640 * lf)))
        lanternPos = (512 - round(640 * lf)) / 2
        self.rendersurf.blit(dark, (lanternPos, lanternPos))


class ViewHolder(object):
    def __init__(self, scale, pos, vp, layer):
        self.scale = scale
        self.pos = pos
        self.viewport = vp
        self.layer = layer
        self.scaled = pygame.Surface((self.viewport.size[0] * self.scale, self.viewport.size[1] * self.scale))

    def draw(self, lf):
        self.viewport.draw(lf)
        img = self.viewport.getRenderSurf().convert()
        pygame.transform.smoothscale(img, (round(self.viewport.size[0] * self.scale), round(self.viewport.size[1] * self.scale)), self.scaled)
        final = defaultPalette(self.scaled)
        final.blit(self.scaled, (0,0))
        DISPLAYSURF.blit(final, self.pos)

    def autoScaleCenter(self):
        W = DISPLAYSURF.get_rect().w
        H = DISPLAYSURF.get_rect().h

        ratio = self.viewport.size[0]/self.viewport.size[1]
        ratio2 = W/H

        if ratio > ratio2:
            #print("wider")
            self.scale = W / self.viewport.size[0]
        else:
            #print("taller")
            self.scale = H / self.viewport.size[1]

        s = (self.viewport.size[0] * self.scale, self.viewport.size[1] * self.scale)
        self.scaled = pygame.Surface(s)
        self.pos = ((W - s[0]) / 2, (H - s[1]) / 2)

    def toVPspace(self, coords):
        shifted = coords - self.pos
        scaled = shifted / self.scale
        return scaled

class ViewLayout(object):
    def __init__(self, vhs):
        self.viewholds = vhs

    def draw(self, lf):
        for vh in self.viewholds:
            vh.draw(lf)
