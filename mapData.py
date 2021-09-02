import sys
import math
import pygame

import map

def makeMap0():
    theMap = map.Map((24, 24), "Surface")

    # floor configs
    fgrs = { "imageName": "textures/floorGrass.png", "image": pygame.image.load("textures/floorGrass.png") }
    fgpc = { "imageName": "textures/floorPathTurn.png", "image": pygame.image.load("textures/floorPathTurn.png"), "rotate": True }
    fgpl = { "imageName": "textures/floorPathLine.png", "image": pygame.image.load("textures/floorPathLine.png"), "rotate": True }
    fgpe = { "imageName": "textures/floorPathEnd.png", "image": pygame.image.load("textures/floorPathEnd.png"), "rotate": True }

    fgse = { "imageName": "textures/floorGrassStone.png", "image": pygame.image.load("textures/floorGrassStone.png"), "rotate": True }
    fstn = { "imageName": "textures/floorStone.png", "image": pygame.image.load("textures/floorStone.png") }
    fbrk = { "imageName": "textures/floorBrick.png", "image": pygame.image.load("textures/floorBrick.png") }
    fbrs = { "imageName": "textures/floorBrickStair.png", "image": pygame.image.load("textures/floorBrickStair.png"), "rotate": True }

    ls = [
        # hallway
        {"pos": map.MapPos(theMap, (17, 2), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (18, 2), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (17, 3), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (17, 4), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (17, 5), 0), "config": fbrk},

        # main chamber entryway
        {"pos": map.MapPos(theMap, (5, 8), 0), "config": fbrk},

        {"pos": map.MapPos(theMap, (6, 7), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (6, 8), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (6, 9), 0), "config": fbrk},

        {"pos": map.MapPos(theMap, (7, 7), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (7, 8), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (7, 9), 0), "config": fbrk},

        {"pos": map.MapPos(theMap, (20, 7), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (20, 8), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (20, 9), 0), "config": fbrk},

        # hallway
        {"pos": map.MapPos(theMap, (5, 9), 0), "config": fstn},

        {"pos": map.MapPos(theMap, (5, 10), 0), "config": fstn},
        {"pos": map.MapPos(theMap, (6, 10), 0), "config": fstn},

        {"pos": map.MapPos(theMap, (5, 11), 0), "config": fbrk},
        {"pos": map.MapPos(theMap, (6, 11), 0), "config": fstn},

        {"pos": map.MapPos(theMap, (5, 12), 0), "config": fstn},
        {"pos": map.MapPos(theMap, (6, 12), 0), "config": fstn},

        {"pos": map.MapPos(theMap, (5, 13), 0), "config": fstn},
        {"pos": map.MapPos(theMap, (6, 13), 0), "config": fstn},

        {"pos": map.MapPos(theMap, (5, 14), 0), "config": fstn},
        {"pos": map.MapPos(theMap, (6, 14), 0), "config": fstn},

        {"pos": map.MapPos(theMap, (5, 15), 3), "config": fgse},
        {"pos": map.MapPos(theMap, (6, 15), 0), "config": fstn},

        # outdoors
        {"pos": map.MapPos(theMap, (0, 12), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 13), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 13), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 13), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 14), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 14), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 14), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 14), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 15), 1), "config": fgpl},
        {"pos": map.MapPos(theMap, (1, 15), 0), "config": fgpc},
        {"pos": map.MapPos(theMap, (2, 15), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 15), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 15), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 16), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 16), 2), "config": fgpc},
        {"pos": map.MapPos(theMap, (2, 16), 1), "config": fgpl},
        {"pos": map.MapPos(theMap, (3, 16), 1), "config": fgpl},
        {"pos": map.MapPos(theMap, (4, 16), 0), "config": fgpc},
        {"pos": map.MapPos(theMap, (5, 16), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (6, 16), 3), "config": fgse},

        {"pos": map.MapPos(theMap, (0, 17), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 17), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 17), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 17), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 17), 2), "config": fgpl},
        {"pos": map.MapPos(theMap, (5, 17), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (6, 17), 2), "config": fgpe},
        {"pos": map.MapPos(theMap, (7, 17), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 18), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 18), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 18), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 18), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 18), 0), "config": fgpe},
        {"pos": map.MapPos(theMap, (5, 18), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (6, 18), 0), "config": fgpl},
        {"pos": map.MapPos(theMap, (7, 18), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (8, 18), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (5, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (6, 19), 0), "config": fgpl},
        {"pos": map.MapPos(theMap, (7, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (8, 19), 3), "config": fgse},

        {"pos": map.MapPos(theMap, (0, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (5, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (6, 19), 0), "config": fgpl},
        {"pos": map.MapPos(theMap, (7, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (8, 19), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (9, 19), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 20), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 20), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 20), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 20), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 20), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (5, 20), 2), "config": fgpe},
        {"pos": map.MapPos(theMap, (6, 20), 0), "config": fgpe},
        {"pos": map.MapPos(theMap, (7, 20), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (8, 20), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (9, 20), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 21), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 21), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 21), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 21), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 21), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (5, 21), 2), "config": fgpc},
        {"pos": map.MapPos(theMap, (6, 21), 0), "config": fgpc},
        {"pos": map.MapPos(theMap, (7, 21), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (8, 21), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (9, 21), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 22), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 22), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 22), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 22), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 22), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (5, 22), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (6, 22), 0), "config": fgpe},
        {"pos": map.MapPos(theMap, (7, 22), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (8, 22), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (9, 22), 0), "config": fgrs},

        {"pos": map.MapPos(theMap, (0, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (1, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (2, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (3, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (4, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (5, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (6, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (7, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (8, 23), 0), "config": fgrs},
        {"pos": map.MapPos(theMap, (9, 23), 0), "config": fgrs},
    ]

    # stairs room
    for x in range(19,24):
        for y in range(5):
            if x == 21 and y == 2:
                ls.append( {"pos": map.MapPos(theMap, (21, 2), 1), "config": fbrs} )
            else:
                ls.append( {"pos": map.MapPos(theMap, (x, y), 0), "config": fbrk} )

    # main chamber
    for x in range(8,20):
        for y in range(6,11):
            ls.append( {"pos": map.MapPos(theMap, (x, y), 0), "config": fbrk} )


    finFloorLs = []
    for d in ls:
        flr = map.Floor.make(**d)
        finFloorLs.append(flr)

    theMap.setFloors(finFloorLs)

    # wall configs
    wbrk = {"imageName": "textures/wallBrick.png", "image": pygame.image.load("textures/wallBrick.png")}
    wbsm = {"imageName": "textures/wallBrickStatMage.png", "image": pygame.image.load("textures/wallBrickStatMage.png")}
    wbsl = {"imageName": "textures/wallBrickStatLampR.png", "image": pygame.image.load("textures/wallBrickStatLampR.png")}
    wbpl = {"imageName": "textures/wallBrickPillars.png", "image": pygame.image.load("textures/wallBrickPillars.png"), "passable": True, "seeThrough": True}
    wstn = {"imageName": "textures/wallStone.png", "image": pygame.image.load("textures/wallStone.png")}
    wmtn = {"imageName": "textures/wallMountain.png", "image": pygame.image.load("textures/wallMountain.png")}

    ls = [
        {"pos": map.MapPos(theMap, (0,12), 2), "config": wmtn},
        {"pos": map.MapPos(theMap, (0,12), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (1,13), 2), "config": wmtn},

        {"pos": map.MapPos(theMap, (2,13), 2), "config": wmtn},
        {"pos": map.MapPos(theMap, (2,13), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (3,14), 2), "config": wmtn},
        {"pos": map.MapPos(theMap, (3,14), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (4,15), 2), "config": wmtn},

        {"pos": map.MapPos(theMap, (6,16), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (7,17), 2), "config": wmtn},
        {"pos": map.MapPos(theMap, (7,17), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (8,18), 2), "config": wmtn},
        {"pos": map.MapPos(theMap, (8,18), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (8,19), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (9,20), 2), "config": wmtn},
        {"pos": map.MapPos(theMap, (9,20), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (9,21), 3), "config": wmtn},
        {"pos": map.MapPos(theMap, (9,22), 3), "config": wmtn},
        {"pos": map.MapPos(theMap, (9,23), 3), "config": wmtn},

        {"pos": map.MapPos(theMap, (5,8), 2), "config": wbrk},

        {"pos": map.MapPos(theMap, (6,7), 1), "config": wbrk},
        {"pos": map.MapPos(theMap, (6,7), 2), "config": wbrk},

        {"pos": map.MapPos(theMap, (7,7), 2), "config": wbrk},

        {"pos": map.MapPos(theMap, (8,6), 1), "config": wbrk},

        {"pos": map.MapPos(theMap, (7,9), 0), "config": wbrk},

        {"pos": map.MapPos(theMap, (8,10), 1), "config": wbrk},

        # mage statues
        {"pos": map.MapPos(theMap, (12,5), 0), "config": wbsm},
        {"pos": map.MapPos(theMap, (14,5), 0), "config": wbsm},
        {"pos": map.MapPos(theMap, (12,11), 2), "config": wbsm},
        {"pos": map.MapPos(theMap, (14,11), 2), "config": wbsm},

        # lamplighter statue
        {"pos": map.MapPos(theMap, (17,2), 2), "config": wbsl},

        # stairs room final
        {"pos": map.MapPos(theMap, (17,2), 1), "config": wbrk},
        {"pos": map.MapPos(theMap, (17,3), 1), "config": wbrk},
        {"pos": map.MapPos(theMap, (17,4), 1), "config": wbrk},
        {"pos": map.MapPos(theMap, (17,5), 1), "config": wbrk},

        {"pos": map.MapPos(theMap, (17,3), 3), "config": wbrk},
        {"pos": map.MapPos(theMap, (17,4), 3), "config": wbrk},
        {"pos": map.MapPos(theMap, (17,5), 3), "config": wbrk},

        {"pos": map.MapPos(theMap, (18,2), 2), "config": wbrk},
        {"pos": map.MapPos(theMap, (18,2), 0), "config": wbrk},

        {"pos": map.MapPos(theMap, (19,6), 3), "config": wbrk},

        {"pos": map.MapPos(theMap, (20,7), 2), "config": wbrk},
        {"pos": map.MapPos(theMap, (20,7), 3), "config": wbrk},

        {"pos": map.MapPos(theMap, (20,8), 3), "config": wbrk},

        {"pos": map.MapPos(theMap, (20,9), 3), "config": wbrk},
        {"pos": map.MapPos(theMap, (20,9), 0), "config": wbrk},

        {"pos": map.MapPos(theMap, (19,10), 3), "config": wbrk},
    ]

    for y in range(8,15):
        ls.append({"pos": map.MapPos(theMap, (5,y), 1), "config": wstn})

    for y in range(10,16):
        ls.append({"pos": map.MapPos(theMap, (6,y), 3), "config": wstn})

    for y in range(6,11):
        ls.append({"pos": map.MapPos(theMap, (10,y), 3), "config": wbpl})
        ls.append({"pos": map.MapPos(theMap, (15,y), 3), "config": wbpl})

    for x in range(8,20):
        if x == 12 or x == 14:
            pass
        elif x == 17:
            pass
        else:
            ls.append({"pos": map.MapPos(theMap, (x, 5), 0), "config": wbrk})
            ls.append({"pos": map.MapPos(theMap, (x, 11), 2), "config": wbrk})

    for x in range(19, 24):
        ls.append({"pos": map.MapPos(theMap, (x, 0), 2), "config": wbrk})
        ls.append({"pos": map.MapPos(theMap, (x, 4), 0), "config": wbrk})

    for y in range(0, 5):
        ls.append({"pos": map.MapPos(theMap, (23, y), 3), "config": wbrk})
        if y != 2:
            ls.append({"pos": map.MapPos(theMap, (19, y), 1), "config": wbrk})

    finWallLs = []
    for d in ls:
        flr = map.Wall.make(**d)
        finWallLs.append(flr)

    theMap.addWalls(finWallLs)

    return theMap


functions = [makeMap0]
