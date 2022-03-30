import pygame
from random import randint
pygame.init()
pygame.font.init()

lung = 800
alt = 800
ris = 6
l = int(lung / ris)
a = int(alt / ris)
lung = l * ris
alt = a * ris

clock = pygame.time.Clock()
screen = pygame.display.set_mode((lung, alt))
done = False


riga = []
lotto = []
newlotto = []
layer = []
newlayer = []
layer2 = []
newlayer2 = []
t = 0
colorr = []
color = []
iterazioni = 0
conto = 0

starve = 4
birth = 4  # Maggiore di 3
iterazioniMax = 15
percMuro = 52
tick = 60

font = pygame.font.SysFont("Calibri", 15)


def ran(n, start1, stop1, start2, stop2):
    return int(((n-start1)/(stop1-start1))*(stop2-start2)+start2)


def drawrect(spigolo, lunghezza, altezza, colore):
    pygame.draw.rect(screen, colore, pygame.Rect(spigolo[0], spigolo[1], lunghezza, altezza))


def testlotto(testX, testY, state):
    countNeigh = 0
    for dx in -1, 0, 1:
        for dy in -1, 0, 1:
            if not (dx == 0 and dy == 0):
                if (testX == 0 or testX == l - 1) or (testY == 0 or testY == a - 1):
                    color[testX][testY] = 90
                    return True
                elif lotto[testX + dx][testY + dy]:
                    countNeigh += 1
    if countNeigh >= starve:
        grad = ran(countNeigh, starve, 8, 60, 100)
        color[testX][testY] = grad
    else:
        color[testX][testY] = 255
    if countNeigh > birth:
        return True
    elif countNeigh < starve:
        return False
    else:
        return state


def testlayer(testX, testY, state):
    countNeigh = 0
    countSupp = 0
    for dx in -2, -1, 0, 1, 2:
        for dy in -2, -1, 0, 1, 2:
            if lotto[testX][testY]:
                if (testX == 0 or testX == l - 1) or (testY == 0 or testY == a - 1):
                    return True
                elif testX + dx < 0 or testX + dx > l - 1 or testY + dy < 0 or testY + dy > a - 1:
                    countSupp += 1
                elif lotto[testX + dx][testY + dy]:
                    countSupp += 1
    for dx in -1, 0, 1:
        for dy in -1, 0, 1:
            if not (dx == 0 and dy == 0):
                if layer[testX + dx][testY + dy]:
                    countNeigh += 1
    if countSupp > 23 and countNeigh > 4:
        return True
    elif countSupp < 23 or countNeigh < 4:
        return False
    else:
        return state


def testlayer2(testX, testY, state):
    countNeigh = 0
    countSupp = 0
    for dx in -2, -1, 0, 1, 2:
        for dy in -2, -1, 0, 1, 2:
            if layer[testX][testY]:
                if (testX == 0 or testX == l - 1) or (testY == 0 or testY == a - 1):
                    return True
                elif testX + dx < 0 or testX + dx > l - 1 or testY + dy < 0 or testY + dy > a - 1:
                    countSupp += 1
                elif layer[testX + dx][testY + dy]:
                    countSupp += 1
    for dx in -1, 0, 1:
        for dy in -1, 0, 1:
            if not (dx == 0 and dy == 0):
                if layer2[testX + dx][testY + dy]:
                    countNeigh += 1
    if countSupp > 24 and countNeigh > 4:
        return True
    elif countSupp < 24 or countNeigh < 4:
        return False
    else:
        return state


for i in range(l):
    riga = []
    colorr = []
    for j in range(a):
        rand = randint(0, 100)
        if rand < percMuro:
            riga.append(True)
            colorr.append(0)
        else:
            riga.append(False)
            colorr.append(255)
    lotto.append(riga)
    color.append(colorr)
newlotto = lotto

for i in range(l):
    riga = []
    for j in range(a):
        rand = randint(0, 100)
        riga.append(True)
    layer.append(riga)
newlayer = layer

for i in range(l):
    riga = []
    for j in range(a):
        rand = randint(0, 100)
        riga.append(True)
    layer2.append(riga)
newlayer2 = layer2

for i in range(iterazioniMax):
    for i in range(l):
        for j in range(a):
            newlotto[i][j] = testlotto(i, j, lotto[i][j])
    lotto = newlotto

for i in range(iterazioniMax):
    for i in range(l):
        for j in range(a):
            newlayer[i][j] = testlayer(i, j, layer[i][j])
    layer = newlayer

for i in range(iterazioniMax):
    for i in range(l):
        for j in range(a):
            newlayer2[i][j] = testlayer2(i, j, layer2[i][j])
    layer2 = newlayer2

screen.fill([0, 0, 100])
for i in range(l):
    for j in range(a):
        if lotto[i][j]:
            drawrect((i * ris, j * ris), ris, ris, (0, color[i][j], 0))
        if layer[i][j]:
            drawrect((i * ris, j * ris), ris, ris, (0, 50, 0))
        if layer2[i][j]:
            drawrect((i * ris, j * ris), ris, ris, (0, 30, 0))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
    clock.tick(tick)
