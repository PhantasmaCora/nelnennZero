#!/usr/bin/env python
import sys
import math
import pygame
import copy

from constants import *

import gameObj

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

        self.lampFactor = 0
        self.noisePos = [0,0]

    def update(self):
        f = random.random() / 2
        self.lampFactor += f ** 3

        self.noisePos[0] += (round(20 * random.random()) - 10) * 4
        self.noisePos[1] += (round(20 * random.random()) - 10) * 4
        if self.noisePos[0] > 1023:
            self.noisePos[0] = 0
        if self.noisePos[0] < 0:
            self.noisePos[0] = 1023
        if self.noisePos[1] > 1023:
            self.noisePos[1] = 0
        if self.noisePos[1] < 0:
            self.noisePos[1] = 1023

    def draw(self):
        self.rendersurf.fill((0,0,0))
        # check whether cached terrain images are still correct
        if not self.mapPos == self.cachePos:
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

            # draw walls and static object panes
            # 1. acquire panes to list
            ls = []
            for offset in camZoneWall[self.mapPos.facing]:
                pos = [self.mapPos.xy[0], self.mapPos.xy[1]]
                pos[0] += offset[0]
                pos[1] += offset[1]
                try:
                    ls.extend(self.mapPos.map.staticObjects[tuple(pos)].panes)
                except KeyError:
                    pass
                ls.extend(self.mapPos.map.getWalls(tuple(pos)))
            # 2. acquire images from panes
            ls2 = []
            for pane in ls:
                ls2.append(pane.getView(self.mapPos))
            ls2.sort(key=lambda tup: tup[1]) # sort by z-level, putting furthest away at start of list
            for tup in ls2:
                self.cached.blit(tup[0], (0,0))

        # blit terrain cache to rendering surface
        self.rendersurf.blit(self.cached, (0,0))

        # blit non-static objects (and obscuring walls)
        # 1. acquire panes to list
        ls = []
        for offset in camZoneWall[self.mapPos.facing]:
            pos = [self.mapPos.xy[0], self.mapPos.xy[1]]
            pos[0] += offset[0]
            pos[1] += offset[1]
            try:
                ls.extend(self.mapPos.map.allObjects[tuple(pos)].panes)
            except KeyError:
                pass
            ls.extend(self.mapPos.map.getWalls(tuple(pos)))
        # 2. acquire images from panes. redraw only walls that may cover an object.
        ls2 = []
        draw = False
        for pane in ls:
            if not draw and isinstance(pane, gameObj.ObjectPane):
                draw = True
            if draw:
                ls2.append(pane.getView(self.mapPos))
        ls2.sort(key=lambda tup: tup[1]) # sort by z-level, putting furthest away at start of list
        for tup in ls2:
            self.cached.blit(tup[0], (0,0))

        # add noise layer
        self.rendersurf.blit(noise, (-self.noisePos[0], -self.noisePos[1]))
        if self.noisePos[0] > 1024 - 512:
            self.rendersurf.blit(noise, (-self.noisePos[0] + 1024, -self.noisePos[1]))
        if self.noisePos[1] > 1024 - 512:
            self.rendersurf.blit(noise, (-self.noisePos[0], -self.noisePos[1] + 1024))
        if self.noisePos[1] > 1024 - 512 and self.noisePos[0] > 1024 - 512:
            self.rendersurf.blit(noise, (-self.noisePos[0] + 1024, -self.noisePos[1] + 1024))

        # final step - render lantern darkness
        lampScale = 0.05 * math.sin(self.lampFactor) + 1
        dark = pygame.transform.smoothscale(lanternImg, (round(640 * lampScale), round(640 * lampScale)))
        lanternPos = (512 - round(640 * lampScale)) / 2
        self.rendersurf.blit(dark, (lanternPos, lanternPos))

class ViewHolder(object):
    def __init__(self, scale, pos, vp, layer):
        self.scale = scale
        self.smallScale = 0.33333
        self.pos = pos
        self.viewport = vp
        self.layer = layer
        self.scaled = pygame.Surface( (round(self.viewport.size[0] * self.scale + self.scale / self.smallScale), round(self.viewport.size[1] * self.scale + self.scale / self.smallScale)) )

        self.small = pygame.Surface((round(self.viewport.size[0] * self.smallScale) + 1, round(self.viewport.size[1] * self.smallScale) + 1))

        self.shift = 0
        self.intShift = 0
        self.scaler = pygame.Surface((self.viewport.size[0] + round(1 / self.smallScale), self.viewport.size[1] + round(1 / self.smallScale)))

    def draw(self):
        self.viewport.draw()
        self.intShift += (random.random() - 0.5)
        if random.random() > 0.95:
            self.smallScale += (random.random() - 0.5) / 4
            self.smallScale = clamp(self.smallScale, 0.2, 0.6)
            self.small = pygame.Surface((round(self.viewport.size[0] * self.smallScale) + 1, round(self.viewport.size[1] * self.smallScale) + 1))
            self.scaled = pygame.Surface((round(self.viewport.size[0] * self.scale + self.scale / self.smallScale), round(self.viewport.size[1] * self.scale + self.scale / self.smallScale)))
        self.shift = round(self.intShift) % round(1 / self.smallScale)
        self.scaler.blit(self.viewport.getRenderSurf(), (self.shift, self.shift))

        pygame.transform.smoothscale(self.scaler, (round(self.viewport.size[0] * self.smallScale) + 1, round(self.viewport.size[1] * self.smallScale) + 1), self.small)

        pygame.transform.smoothscale(self.small, (round(self.viewport.size[0] * self.scale + self.scale / self.smallScale), round(self.viewport.size[1] * self.scale + self.scale / self.smallScale)), self.scaled)

        final = pygame.Surface((round(self.viewport.size[0] * self.scale), round(self.viewport.size[1] * self.scale)))
        final = defaultPalette(final)
        final.blit(self.scaled, (0,0), (self.shift, self.shift, final.get_rect().w, final.get_rect().h))
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

        s = (round(self.viewport.size[0] * self.scale + self.scale / self.smallScale), round(self.viewport.size[1] * self.scale + self.scale / self.smallScale))
        self.scaled = pygame.Surface(s)
        self.pos = ((W - s[0]) / 2, (H - s[1]) / 2)

    def toVPspace(self, coords):
        shifted = coords - self.pos
        scaled = shifted / self.scale
        return scaled

class ViewLayout(object):
    def __init__(self, vhs):
        self.viewholds = vhs

    def draw(self):
        for vh in self.viewholds:
            vh.draw()
