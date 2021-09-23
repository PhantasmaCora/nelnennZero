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
noise = pygame.transform.smoothscale(noise, (1024, 1024))

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
        (214, 171, 22),
        (173, 110, 20),
        (146, 67, 20),
        (110, 47, 30),
        (134, 42, 40),
        (164, 54, 78),
        (197, 102, 135),
        (199, 139, 173),
        (40, 26, 30),
        (57, 37, 40),
        (88, 60, 57),
        (107, 81, 70),
        (19, 21, 26),
        (36, 26, 46),
        (60, 27, 71),
        (92, 12, 81),
        (160, 190, 111),
        (155, 170, 68),
        (158, 142, 41),
        (143, 117, 28),
        (129, 90, 23),
        (162, 92, 32),
        (200, 101, 32),
        (213, 91, 26),
        (40, 35, 26),
        (55, 57, 37),
        (75, 88, 57),
        (78, 107, 70),
        (26, 19, 21),
        (46, 26, 26),
        (71, 38, 27),
        (92, 63, 12),
        (7, 18, 54),
        (13, 49, 100),
        (19, 87, 127),
        (25, 99, 126),
        (34, 116, 118),
        (54, 164, 140),
        (102, 197, 164),
        (139, 199, 165),
        (26, 40, 40),
        (37, 48, 57),
        (57, 64, 88),
        (76, 70, 107),
        (25, 26, 19),
        (36, 46, 26),
        (38, 71, 27),
        (12, 92, 23),
        (214, 22, 69),
        (173, 20, 85),
        (129, 24, 91),
        (106, 27, 86),
        (118, 34, 118),
        (131, 52, 155),
        (158, 124, 179),
        (180, 173, 194),
        (47, 49, 64),
        (63, 57, 79),
        (93, 77, 105),
        (119, 89, 121),
        (3, 3, 3),
        (26, 27, 46),
        (36, 27, 71),
        (59, 12, 92)
    ]
    )
    return nsurface
