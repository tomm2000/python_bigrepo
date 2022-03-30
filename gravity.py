import pygame
from pygame import gfxdraw as gfx
from math import sqrt as sqrt
from math import cos as cos
from math import sin as sin
from math import atan2 as atan2
# from random import randint
from math import pi
# from math import degrees as deg
from math import radians as rad
pygame.init()
pygame.font.init()

lung = 1200
alt = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((lung, alt))
done = False

bianco = (255, 255, 255)
neroleg = (0, 0, 0, 150)
blu = (0, 0, 255)
nero = (0, 0, 0)
grigio = (150, 150, 150)
rosso = (255, 0, 0)
verde = (0, 255, 0)
tick = 60
grav = 35
camera = [0, 0]
densita = 4
font10 = pygame.font.SysFont("Calibri", 13)
font15 = pygame.font.SysFont("Calibri", 15)
font20 = pygame.font.SysFont("Calibri", 20)
s1 = False
s2 = False
s3 = False
s4 = False
s5 = False
s6 = False
following = False
followed = 0


def drawball(center, raggio, colore):
    gfx.aacircle(screen, round(center[0]) + camera[0], round(center[1]) + camera[1], round(raggio), colore)
    gfx.filled_circle(screen, round(center[0]) + camera[0], round(center[1]) + camera[1], round(raggio), colore)


def drawline(punto1, punto2, colore):
    gfx.line(screen, round(punto1[0]) + camera[0], round(punto1[1] + camera[1]), round(punto2[0]) + camera[0], round(punto2[1]) + camera[1], colore)


def drawrect(spigolo, l, a, colore):
    pygame.draw.rect(screen, colore, pygame.Rect(spigolo[0] + camera[0], spigolo[1] + camera[1], l, a))


def drawvect(p, mod, ang, colore):
    gfx.line(screen, round(p[0]) + camera[0], round(p[1]) + camera[1], round((cos(ang) * mod) + p[0]) + camera[0],  round(- (sin(ang) * mod) + p[1]) + camera[1], colore)


def angle(p1, p2):
    if p1[0] == p2[0]:
        if p1[1] < p2[1]:
            return pi / 2
        else:
            return 3 * pi / 2
    else:
        return -atan2(p2[1] - p1[1], p2[0] - p1[0]) + pi


def dist(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


def sommavettori(v1, v2):
    vtx = ((cos(v1[1]) * v1[0]) + (cos(v2[1]) * v2[0]))
    vty = ((sin(v1[1]) * v1[0]) + (sin(v2[1]) * v2[0]))
    vt = sqrt((vtx ** 2) + (vty ** 2))
    if vtx == 0:
        return [vt, 0]
    else:
        return [vt, atan2(vty, vtx)]


class CorpiStatici:
    def __init__(self, posizione, massa):
        self.pos = posizione
        self.r = (massa ** (1 / 3)) * densita
        self.m = massa

    def draw(self):
        drawball(self.pos, self.r, nero)


statici = [CorpiStatici([500, 400], 700)]
# statici.append(CorpiStatici([5000, 400], 700))


class Mobile:
    def __init__(self, posizione, massa, velocita):
        self.pos = posizione
        self.r = (massa ** (1 / 3)) * densita
        self.m = massa
        self.v = velocita
        self.f = [0, 0]
        self.a = [0, 0]
        self.hit = False

    def fisica(self):

        self.f = [0, 0]
        self.a = [0, 0]
        for i in range(len(statici)):
            angolo = angle(self.pos, statici[i].pos)
            distanza = dist(self.pos, statici[i].pos) * 6
            if distanza == 0:
                gravita = 0
            else:
                gravita = (self.m * statici[i].m) / (distanza ** 2) * grav
            self.f = sommavettori(self.f, (gravita, angolo))
            if dist(self.pos, statici[i].pos) <= statici[i].r + self.r:
                self.v = [0, 0]
                self.a = [0, 0]
                self.f = [0, 0]
                self.hit = True

        if not self.hit:
            self.a = sommavettori(self.a, self.f)
            self.a[0] = self.a[0] / self.m
            self.v = sommavettori(self.v, self.a)
            self.pos = ((- cos(self.v[1]) * self.v[0]) + self.pos[0], self.pos[1] + (sin(self.v[1]) * self.v[0]))
            if pressed[pygame.K_SPACE]:
                drawvect(self.pos, (self.f[0] * 50000) ** (1 / 3), self.f[1] + pi, rosso)
                drawvect(self.pos, self.v[0] * 30, self.v[1] + pi, verde)

    def draw(self):
        drawball(self.pos, self.r, nero)


mobili = []
mobili.append(Mobile([450, 400], 7, [3.7, rad(90)]))
mobili.append(Mobile([350, 400], 7, [2.9, rad(-90)]))
mobili.append(Mobile([500, 445], 7, [5.2, rad(0)]))
mobili.append(Mobile([100, 400], 7, [1.2, rad(-90)]))
mobili.append(Mobile([-200, 400], 7, [0.98, rad(-90)]))
mobili.append(Mobile([-1000, 400], 7, [0.2, rad(-90)]))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(bianco)
    pressed = pygame.key.get_pressed()
    mouse = (pygame.mouse.get_pos()[0] - camera[0], pygame.mouse.get_pos()[1] - camera[1])
    if pygame.mouse.get_pressed()[0]:
        drawball(mouse, 3, rosso)

    if not following:
        if pressed[pygame.K_a]:
            camera = (camera[0] + round(600 / tick), camera[1])
        if pressed[pygame.K_d]:
            camera = (camera[0] - round(600 / tick), camera[1])
        if pressed[pygame.K_w]:
            camera = (camera[0], camera[1] + round(600 / tick))
        if pressed[pygame.K_s]:
            camera = (camera[0], camera[1] - round(600 / tick))

    if pressed[pygame.K_UP] and not s1:
        following = True
        s1 = True
        followed += 1
        if followed > len(mobili) - 1:
            followed = 0
    elif not pressed[pygame.K_UP]:
        s1 = False

    if pressed[pygame.K_DOWN] and not s5:
        following = True
        s5 = True
        followed -= 1
        if followed < 0:
            followed = len(mobili) - 1
    elif not pressed[pygame.K_DOWN]:
        s5 = False

    if pressed[pygame.K_KP0] and not s2:
        s2 = True
        if following:
            following = False
        else:
            following = True
    elif not pressed[pygame.K_KP0]:
        s2 = False

    if pressed[pygame.K_RIGHT] and not s3:
        s3 = True
        tick += 10
        if tick > 300:
            tick = 30
    elif not pressed[pygame.K_RIGHT]:
        s3 = False

    if pressed[pygame.K_LEFT] and not s4:
        s4 = True
        tick -= 10
        if tick < 30:
            tick = 300
    elif not pressed[pygame.K_LEFT]:
        s4 = False

    if following:
        camera = (round(lung / 2) - round(mobili[followed].pos[0]), round(alt / 2) - round(mobili[followed].pos[1]))

    for i in range(len(statici)):
        statici[i].draw()
        if pressed[pygame.K_SPACE]:
            screen.blit(font10.render("Massa: " + str(statici[i].m), True, nero), (statici[i].pos[0] + camera[0] - 30, statici[i].pos[1] + camera[1] - 5))

    for i in range(len(mobili)):
        mobili[i].fisica()
        mobili[i].draw()
        if pressed[pygame.K_SPACE]:
            screen.blit(font15.render("Vel: " + str(round(mobili[i].v[0], 2)), True, nero), (mobili[i].pos[0] - 25 + camera[0], mobili[i].pos[1] - 25 + camera[1]))
    if following and pressed[pygame.K_SPACE]:
        screen.blit(font20.render("Velocità: " + str(round(mobili[followed].v[0], 10)), True, nero), ((lung / 2) - 60, 0))
        screen.blit(font20.render("Accelerazione (x100): " + str(round(mobili[followed].a[0], 10)), True, nero), ((lung / 2) - 110, 20))
        screen.blit(font20.render("Forza tot (x100): " + str(round(mobili[followed].f[0], 10)), True, nero), ((lung / 2) - 100, 40))

    if following:
        screen.blit(font20.render("Pos = X: " + str(-camera[0] + round(lung / 2)) + " | Y: " + str(-camera[1] + round(alt / 2)), True, nero), (0, 0))
    else:
        screen.blit(font20.render("Pos = X: " + str(-camera[0]) + " | Y: " + str(-camera[1]), True, nero), (0, 0))
    screen.blit(font20.render("Following: " + str(following) + " | N: " + str(followed + 1), True, nero), (0, 20))
    screen.blit(font20.render("Tick: " + str(tick), True, nero), (0, 40))
    pygame.display.flip()
    clock.tick(tick)
