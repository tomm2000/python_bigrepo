import pygame
from pygame import draw
from pygame import gfxdraw as gfx
from math import sqrt as sqrt
from math import cos as cos
from math import sin as sin
from math import atan2 as atan2
from random import randint
from math import pi
from math import degrees as deg
from math import radians as rad

pygame.init()
pygame.font.init()

# COLORI: ----------
bianco = (255, 255, 255)
blu = (0, 0, 255)
nero = (0, 0, 0)
grigio = (150, 150, 150)
rosso = (255, 0, 0)
verde = (0, 255, 0)
# ------------------

# COSTANTI ---------
grav = 35
dens = 6
zoom = 1
distmolt = 6
# ------------------

# BASE -------------
tick = 60
lung = 1200
alt = 800
done = False
screen = pygame.display.set_mode((lung, alt))
clock = pygame.time.Clock()
# ------------------

# ALTRE VARIABILI --
camera = [0, 0]
angolo = 1
modulo = 0
x = 0
y = 1
corpi = []
s1 = False
s2 = False
s3 = False
s4 = False
s5 = False
s6 = False
# ------------------

# FONT -------------
font10 = pygame.font.SysFont("Calibri", 13)
font15 = pygame.font.SysFont("Calibri", 15)
font20 = pygame.font.SysFont("Calibri", 20)
# ------------------


def drawball(centro, raggio, colore):
    gfx.aacircle(screen, round(centro[x] + camera[x]), round(centro[y] + camera[y]), round(raggio), colore)


def drawaball(centro, raggio, colore):
    if raggio < 1:
        raggio = 1
    pygame.draw.circle(screen, colore, (round(centro[x] + camera[x]), round(centro[y] + camera[y])), round(raggio), 1)


def drawline(punto1, punto2, colore):
    gfx.line(screen, round(punto1[0] + camera[0]), round(punto1[1] + camera[1]), round(punto2[0] + camera[0]), round(punto2[1] + camera[1]), colore)


def drawvect(centro, modulo, angolo, colore):
    gfx.line(screen, round(centro[0] + camera[0]), round(centro[1] + camera[1]), round((cos(angolo) * modulo) + centro[0] + camera[0]), round(- (sin(angolo) * modulo) + centro[1] + camera[1]), colore)


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


class Corpi:
    def __init__(self, posizione, velocita, massa):
        self.pos = posizione
        self.vel = velocita
        self.mas = massa
        self.r_or = round((massa ** (1 / 3)) * dens, 2)
        self.r = round(self.r_or / zoom, 1)
        self.f = [0, 0]
        self.a = [0, 0]
        self.soi = ((self.mas ** 2) * grav) / (distmolt * 1200)
        if self.soi < self.r_or:
            self.soi = self.r_or + 5

    def fisica(self):
        self.f = [0, 0]
        self.a = [0, 0]
        self.r = round(self.r_or / zoom, 1)
        for i in range(len(corpi)):
            d = dist(self.pos, corpi[i].pos) * zoom * distmolt
            if 0 < d / distmolt < corpi[i].soi:
                a = angle(self.pos, corpi[i].pos)
                fg = (self.mas * corpi[i].mas) / (d ** 2) * grav
                self.f = sommavettori(self.f, (fg, a))
        self.a = ((self.f[modulo] / self.mas), self.f[angolo])
        self.vel = sommavettori(self.vel, self.a)
        self.pos = ((self.pos[x] - cos(self.vel[angolo]) * self.vel[modulo] / zoom), self.pos[y] + (sin(self.vel[angolo]) * self.vel[modulo] / zoom))

    def draw(self):
        drawball((self.pos[x] / zoom, self.pos[y] / zoom), self.r, nero)
        if pressed[pygame.K_SPACE]:
            drawvect(self.pos, (self.f[modulo] * 50000) ** (1 / 3), self.f[angolo] + pi, rosso)
            drawvect(self.pos, self.vel[modulo] * 30, self.vel[angolo] + pi, verde)
            screen.blit(font15.render("Vel: " + str(round(self.vel[modulo], 2)), True, nero), (self.pos[x] - 25 + camera[x], self.pos[y] - 25 + camera[y]))
            screen.blit(font15.render("Soi: " + str(round(self.soi)), True, nero), (self.pos[x] - 25 + camera[x], self.pos[y] - 45 + camera[y]))
            drawaball(self.pos, self.soi, rosso)


corpi.append(Corpi((600, 600), [0.5, 0], 400))
# corpi.append(Corpi((3000, 400), [0, 0], 500))
corpi.append(Corpi((200, 200), [0.5, rad(180)], 400))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(bianco)
    pressed = pygame.key.get_pressed()
    mouse = (pygame.mouse.get_pos()[0] - camera[0], pygame.mouse.get_pos()[1] - camera[1])
    if pygame.mouse.get_pressed()[0]:
        drawball(mouse, 3, rosso)

    if pressed[pygame.K_a]:
        camera = (camera[0] + round(600 / tick), camera[1])
    if pressed[pygame.K_d]:
        camera = (camera[0] - round(600 / tick), camera[1])
    if pressed[pygame.K_w]:
        camera = (camera[0], camera[1] + round(600 / tick))
    if pressed[pygame.K_s]:
        camera = (camera[0], camera[1] - round(600 / tick))


    # if pressed[pygame.K_UP]:
    #     zoom += 0.02
    #     if zoom > 20:
    #         zoom = 1
    #
    # if pressed[pygame.K_DOWN] and not s2:
    #     zoom -= 0.02
    #     if zoom < 1:
    #         zoom = 20
    #
    # zoom = round(zoom, 2)

    for i in range(len(corpi)):
        corpi[i].fisica()
        corpi[i].draw()
    pygame.display.flip()
    clock.tick(tick)
