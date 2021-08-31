
import math
import pygame

def floor_transform(img, corners, tb):
    mx = max(corners)
    my = max(tb) + 1
    height = tb[1] - tb[0]

    new = pygame.Surface((mx,my))

    sc = pygame.transform.smoothscale(img, (img.get_rect().w, height))

    for rowIndex in range(height):
        frac = rowIndex / height
        ls = round(frac * corners[2] + (1 - frac) * corners[0])
        rs = round(frac * corners[3] + (1 - frac) * corners[1])
        rec = pygame.Rect(0, rowIndex, sc.get_rect().w, 1)
        rowPreScale = pygame.Surface((rec.w, rec.h))
        rowPreScale.blit(sc, (0,0), rec)
        rowPostScale = pygame.transform.smoothscale(rowPreScale, (rs - ls, 1))
        new.blit(rowPostScale, (ls, rowIndex + tb[0]))

    return new

def wall_transform(img, corners, lr):
    my = max(corners)
    mx = max(lr) + 1
    width = lr[1] - lr[0]

    new = pygame.Surface((mx,my))

    sc = pygame.transform.smoothscale(img, (width, img.get_rect().h))

    for colIndex in range(width):
        frac = colIndex / width
        ts = round(frac * corners[1] + (1 - frac) * corners[0])
        bs = round(frac * corners[3] + (1 - frac) * corners[2])
        rec = pygame.Rect(colIndex, 0, 1, sc.get_rect().h)
        colPreScale = pygame.Surface((rec.w, rec.h))
        colPreScale.blit(sc, (0,0), rec)
        colPostScale = pygame.transform.smoothscale(colPreScale, (1, bs - ts))
        new.blit(colPostScale, (colIndex + lr[0], ts))

    return new
