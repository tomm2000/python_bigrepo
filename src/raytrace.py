import pygame
from math import radians as rad
from math import cos as cos
from math import sin as sin
from math import sqrt as sqrt
from math import atan as atan
from math import degrees as deg
from pygame import gfxdraw as gfx
from random import randint
pygame.init()

# dichiarazaione variabili

lung = 800
alt = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((lung, alt))
pos = ()
nero = (0, 0, 0, 100)
verde = (35, 114, 22)
bianco = (255, 255, 255, 40)
mouse = pygame.mouse.get_pos()
raggi = 40
luce = [400, 400]

done = False


def shift(pos):
    return ran(pos, alt, 0, 0, alt)

def ran(n, start1, stop1, start2, stop2):
    return int(((n-start1)/(stop1-start1))*(stop2-start2)+start2)


def drawball(pos, raggio, colore):
    gfx.aacircle(screen, int(pos[0]), shift(pos[1]), raggio, colore)


def drawline(punto1, punto2, colore):
    gfx.line(screen, int(punto1[0]), int(shift(punto1[1])), int(punto2[0]), int(shift(punto2[1])), colore)


def distanza2p(punto1, punto2):
    return sqrt(((punto2[0] - punto1[0]) ** 2) * ((punto2[1] - punto1[1]) ** 2))


class Muro:
    def __init__(self, punto1, punto2):
        self.p1 = punto1
        self.p2 = punto2

    def draw(self):
        drawline(self.p1, self.p2, verde)


muri = [Muro((0, 0), (800, 0)),  Muro((800, 0), (800, 800)), Muro((800, 800), (0, 800)),  Muro((0, 800), (0, 0)), Muro((100, 700), (500, 700))]
for i in range(15):
    muri.append(Muro((randint(0, 800), randint(0, 800)), (randint(0, 800), randint(0, 800))))


class Ray:
    def __init__(self, punto, angolo):
        self.p1 = punto
        self.ang = angolo


    def hit(self):
        self.hits = []
        self.dist = []
        self.inters = []
        for muro in muri:
            self.p2 = ((self.p1[0] + cos(rad(self.ang)) * 600), (self.p1[1] + sin(rad(self.ang)) * 600))
            self.den = ((self.p1[0] - self.p2[0]) * (muro.p1[1] - muro.p2[1])) - ((self.p1[1] - self.p2[1]) * (muro.p1[0] - muro.p2[0]))
            if not self.den == 0:
                self.tnum = ((self.p1[0] - muro.p1[0]) * (muro.p1[1] - muro.p2[1])) - ((self.p1[1] - muro.p1[1]) * (muro.p1[0] - muro.p2[0]))
                self.unum = ((self.p1[0] - self.p2[0]) * (self.p1[1] - muro.p1[1])) - ((self.p1[1] - self.p2[1]) * (self.p1[0] - muro.p1[0]))
                self.t = self.tnum / self.den
                self.u = self.unum / self.den
                if -1 <= self.u <= 0 and 0 <= self.t <= 1:
                    self.inters.append((self.p1[0] + self.t * (self.p2[0] - self.p1[0]), self.p1[1] + self.t * (self.p2[1] - self.p1[1])))
        for i in range(len(self.inters)):
            if i == 0:
                self.corto = distanza2p(self.p1, self.inters[0])
                self.vicino = self.inters[0]
            elif i > 0 and distanza2p(self.p1, self.inters[i]) < self.corto:
                self.corto = distanza2p(self.p1, self.inters[i])
                self.vicino = self.inters[i]
        if len(self.inters) > 0:
            drawline(self.p1, self.vicino, bianco)
        else:
            drawline(self.p1, self.p2, bianco)




# MAIN GAME LOOP
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    mouse = pygame.mouse.get_pos()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a] and luce[0] > 14:
        luce[0] -= 5
    if pressed[pygame.K_d] and luce[0] < 786:
        luce[0] += 5
    if pressed[pygame.K_w] and luce[1] > 14:
        luce[1] -= 5
    if pressed[pygame.K_s] and luce[1] < 786:
        luce[1] += 5
    if luce[0] == mouse[0]:
        ang = 180
    else:
        if mouse[0] > luce[0]:
            ang = -deg(atan((mouse[1] - luce[1]) / (mouse[0] - luce[0])))
        else:
            ang = -deg(atan((mouse[1] - luce[1]) / (mouse[0] - luce[0]))) + 180
    rays = []
    for i in range(raggi):
        rays.append(Ray((luce[0], shift(luce[1])), ang - (raggi / 2) + i))
    screen.fill(nero)

    for i in range(len(rays)):
        rays[i].hit()

    for i in range(len(muri)):
        muri[i].draw()

    drawball((luce[0], shift(luce[1])), 8, (255, 0, 0))

    pygame.display.flip()
    clock.tick(60)
