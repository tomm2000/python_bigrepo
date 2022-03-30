import pygame
from pygame import gfxdraw as gfx

def drawLinePoints(startX, startY, endX, endY, surface, color):
    gfx.line(surface, int(startX), int(startY), int(endX), int(endY), color)

def drawLineFunc(m, b, maxX, surface, color): #y = mx + b
    gfx.line(surface, 0, int(b), maxX, int(maxX * m + b), color)

def drawCircle(x, y, surface, r, color):
    gfx.aacircle(surface, int(x), int(y), int(r), color)
    gfx.filled_circle(surface, int(x), int(y), int(r), color)

def drawCircleOutline(x, y, surface, r, color):
    gfx.aacircle(surface, int(x), int(y), int(r) + 1, color)

def sign(n):
    if n >= 0: return 1
    else: return -1

def spread(n, start1, stop1, start2, stop2):
    return int(((n-start1)/(stop1-start1))*(stop2-start2)+start2)