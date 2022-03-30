import pygame
from pygame import gfxdraw as gfx
from math import sqrt as sqrt
from math import cos as cos
from math import sin as sin
from math import atan as atan
from random import randint
from math import pi
pygame.init()

lung = 1000
alt = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((lung, alt))
done = False

bianco = (255, 255, 255)
nero = (0, 0, 0, 150)
neropes = (0, 0, 0)
grigio = (150, 150, 150)
rosso = (255, 0, 0)
verde = (0, 255, 0)
pos = [400, 400]
sfere = 400
hit = False
at = 0
tick = 100


def ran(n, start1, stop1, start2, stop2):
    return int(((n-start1)/(stop1-start1))*(stop2-start2)+start2)


def drawball(center, raggio, colore):
    gfx.aacircle(screen, int(center[0]), int(center[1]), int(raggio), colore)


def drawline(punto1, punto2, colore):
    gfx.line(screen, int(punto1[0]), int(punto1[1]), int(punto2[0]), int(punto2[1]), colore)


def drawrect(spigolo, l, a, colore):
    pygame.draw.rect(screen, colore, pygame.Rect(spigolo[0], spigolo[1], l, a))


def dist(angolore, width, height, punto):
    cx = (angolore[0] + (angolore[0] + width)) / 2
    cy = (angolore[1] + (angolore[1] + height)) / 2
    dx = max(abs(punto[0] - cx) - width / 2, 0)
    dy = max(abs(punto[1] - cy) - height / 2, 0)
    return sqrt(dx * dx + dy * dy)


def angle(p1, p2):
    if p2[0] > p1[0] and not p2[0] == p1[0]:
        return atan((p2[1] - p1[1]) / (p2[0] - p1[0]))
    elif p2[0] < p1[0] and not p2[0] == p1[0]:
        return atan((p2[1] - p1[1]) / (p2[0] - p1[0])) + pi
    elif p2[0] == p1[0] and p2[1] > p1[1]:
        return pi / 2
    else:
        return -pi / 2


def intercirc(punto, centro, raggio):
    return [centro[0] + int(cos(angle(centro, punto)) * raggio), centro[1] + int(sin(angle(centro, punto)) * raggio)]


rects = []
for i in range(20):
    rects.append([(randint(0, lung - 200), randint(0, alt - 200)), randint(50, 200), randint(50, 200)])

# ----------Bordi----------

# rects.append([(0, 0), 1, alt])
# rects.append([(0, 0), lung, 1])
# rects.append([(lung, 0), 1, alt])
# rects.append([(0, alt), lung, 1])

# --------------------------

punti = [pos]
for i in range(sfere - 1):
    punti.append([0, 0])


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE]:
        mod = 0.05
    else:
        mod = 1

    if pressed[pygame.K_a]:
        pos[0] -= (int(300 / tick) * mod)
    if pressed[pygame.K_d]:
        pos[0] += (int(300 / tick) * mod)
    if pressed[pygame.K_w]:
        pos[1] -= (int(300 / tick) * mod)
    if pressed[pygame.K_s]:
        pos[1] += (int(300 / tick) * mod)
    mouse = pygame.mouse.get_pos()
    puntom = [pos[0] + int(cos(angle(pos, mouse)) * 3000), pos[1] + int(sin(angle(pos, mouse)) * 3000)]
    screen.fill((255, 255, 255))

    drawball(pos, 3, rosso)
    for i in range(len(rects)):
        drawrect(rects[i][0], rects[i][1], rects[i][2], grigio)

    tot = 0
    i = 0
    while True:
        dists = []
        for j in range(len(rects)):
            dists.append(dist(rects[j][0], rects[j][1], rects[j][2], punti[i]))
        r = min(dists)
        tot += r
        if sqrt(((punti[i][0] - pos[0]) ** 2) + ((punti[i][1] - pos[1]) ** 2)) > 5000:
            break
        if r < 1:
            drawball(punti[i], 4, verde)
            hit = True
            at = i
            break

        # drawball(intercirc(puntom, pos, tot), 2, rosso)

        if i < sfere - 1:
            punti[i + 1] = intercirc(puntom, pos, tot)
        if r < 1000:
            drawball(punti[i], r, nero)
        else:
            break
        hit = False
        i += 1

    if not hit:
        drawline(pos, puntom, neropes)
    else:
        drawline(pos, punti[at], neropes)

    pygame.display.flip()
    clock.tick(tick)
