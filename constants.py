# import relevant thingies
import sys
import random
import math
import pygame
import copy
import itertools

from pygame.math import Vector2 as Vector
from pygame.locals import *

# ---------------------------
# constants.py contains key global values and classless utility functions.
# is it best practices? maybe, maybe not.
# it's mostly worked fine for me in the past...
# ---------------------------

# game dimension constants (internal rendering surface)
W = 1600
H = 1280
FPS = 60 # note to self, if you need a delta-t for whatever reason it's 1/FPS

# initialise pygame
pygame.init()

# create surface for visible display window
DISPLAYSURF = pygame.display.set_mode((800,640), flags=pygame.RESIZABLE)
# and add caption
pygame.display.set_caption('Nelnenn Zero')

# set window icon
#icon = pygame.image.load('textures/icon.bmp').convert()
#pygame.display.set_icon(icon)

# permanent image loading
lanternImg = pygame.image.load("textures/lantern.png")
lanternImg.convert_alpha()

errorTile = pygame.image.load("textures/errorTile.png")
errorTile.convert()

noise = pygame.image.load("textures/noiseBlue.png")
noise.convert()
noise.set_alpha(16)
noise = pygame.transform.scale(noise, (512, 512))

# Important???
clock = pygame.time.Clock()
pygame.mixer.init()

# Grid Reference
cRows = (0, 66, 100, 124, 142) # ceiling close -> far
fRows = (512, 444, 410, 386, 368) # floor close -> far
xCols = (
 (-50, 144, 366, 560), # behind you!
 (2, 170, 340, 510), # closest row
 (48, 186, 324, 462), # second row
 (80, 196, 314, 430), # third row
 (104, 204, 306, 406) # furthest row
)

# Camera Reference
centerLs = [-1, 0, 1]
camNorth = list(itertools.product(centerLs, [-3, -2, -1]))
camEast = list(itertools.product([3, 2, 1], centerLs))
camSouth = list(itertools.product(centerLs, [3, 2, 1]))
camWest = list(itertools.product([-3 ,-2, -1], centerLs))
camZone = [camNorth, camEast, camSouth, camWest]

centerLs = [-2, -1, 0, 1, 2]
camNorthW = list(itertools.product(centerLs, [-4, -3, -2, -1, 0]))
camEastW = list(itertools.product([4, 3, 2, 1, 0], centerLs))
camSouthW = list(itertools.product(centerLs, [4, 3, 2, 1, 0]))
camWestW = list(itertools.product([-4, -3, -2, -1, 0], centerLs))
camZoneWall = [camNorthW, camEastW, camSouthW, camWestW]

# utilities
def clamp(value, mini, maxi):
    return min(maxi, max(value, mini))

# palettes
def defaultPalette(surface):
    nsurface = surface.convert(8)
    nsurface.set_palette(
    [
        (0,0,0),
        (81, 25, 19),
        (118, 44, 19),
        (168, 62, 25),
        (187, 75, 25),
        (218, 106, 19),
        (249, 168, 50),
        (249, 199, 62),
        (249, 236, 193),
        (52, 11, 25),
        (73, 19, 41),
        (97, 42, 59),
        (128, 61, 72),
        (156, 81, 81),
        (185, 117, 104),
        (196, 133, 91),
        (204, 148, 75),
        (93, 50, 131),
        (137, 75, 118),
        (151, 106, 124),
        (160, 127, 136),
        (87, 36, 36),
        (134, 45, 41),
        (170, 40, 29),
        (195, 21, 0),
        (58, 25, 83),
        (105, 29, 98),
        (156, 31, 81),
        (216, 34, 78),
        (12, 6, 62),
        (16, 49, 81),
        (25, 87, 100),
        (37, 112, 118),
        (0, 124, 169),
        (0, 163, 182),
        (0, 195, 195),
        (125, 216, 203),
        (12, 6, 37),
        (20, 29, 56),
        (44, 60, 73),
        (63, 76, 80),
        (59, 72, 43),
        (99, 110, 56),
        (131, 118, 41),
        (149, 103, 37),
        (50, 37, 56),
        (82, 28, 59),
        (149, 19, 68),
        (218, 19, 56),
        (36, 29, 26),
        (59, 48, 46),
        (90, 77, 76),
        (120, 107, 107),
        (0, 56, 57),
        (0, 108, 94),
        (0, 143, 106),
        (0, 177, 104),
        (39, 38, 46),
        (51, 49, 58),
        (63, 58, 67),
        (81, 72, 81),
        (30, 21, 66),
        (62, 36, 104),
        (108, 60, 140),
        (162, 96, 177)
    ]
    )
    return nsurface
