import pygame
from random import randint as randint

xf = 800
yf = 800

pygame.init()
screen = pygame.display.set_mode((xf, yf))
done = False

# larghezza snake
lar = 20

# moltiplicatore movimento
dir = [0, -1]

# pos = [[posizione segmento, x segmento, y segmento],...]
pos = [[0, xf/2, yf/2]]

# dichiarazione variabili [x, y]
cibo = [0, 0]
mov = [0, 0]
tmp = [0, 0]

# ogni quanti tick puoi muoverti
wait = 1
t = 0

# lunghezza snake
lun = 1

for i in range(lun):
    pos.append([(i + 1), int(pos[0][1]), int(pos[i][2]) + lar])

clock = pygame.time.Clock()

cibo[0] = randint(1, xf/lar) * lar
cibo[1] = randint(1, yf/lar) * lar


def scambio():
    for i in range(lun):
        tmp[0] = pos[(i + 1)][1]
        pos[(i + 1)][1] = mov[0]
        mov[0] = tmp[0]

        tmp[1] = pos[(i + 1)][2]
        pos[(i + 1)][2] = mov[1]
        mov[1] = tmp[1]


def checkmuro():
    if mov[1] > yf - lar:
        mov[1] = 0
    if mov[1] < 0:
        mov[1] = yf - lar
    if mov[0] > xf - lar:
        mov[0] = 0
    if mov[0] < 0:
        mov[0] = xf - lar

# GAME CICLE
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # movimento
    if t == 0:
        pressed = pygame.key.get_pressed()

        #movimento sinistra
        if pressed[pygame.K_LEFT]:
            t = wait
            if dir[0] == -1 or dir[1] == 1 or dir[1] == -1:
                dir[0] = -1
                dir[1] = 0
            else:
                dir[0] = 0
                dir[1] = 1

        # movimento destra
        if pressed[pygame.K_RIGHT]:
            t = wait
            if dir[0] == 1 or dir[1] == 1 or dir[1] == -1:
                dir[0] = 1
                dir[1] = 0
            else:
                dir[0] = 0
                dir[1] = 1

        # movimento sù
        if pressed[pygame.K_UP]:
            t = wait
            if dir[1] == -1 or dir[0] == -1 or dir[0] == 1:
                dir[1] = -1
                dir[0] = 0
            else:
                dir[0] = 1
                dir[1] = 0

        # movimento giù
        if pressed[pygame.K_DOWN]:
            t = wait
            if dir[1] == 1 or dir[0] == -1 or dir[0] == 1:
                dir[1] = 1
                dir[0] = 0
            else:
                dir[0] = 1
                dir[1] = 0

    if t > 0:
        t -= 1

    mov[0] = pos[0][1] + (lar * dir[0])
    mov[1] = pos[0][2] + (lar * dir[1])
    checkmuro()
    pos[0][1] = mov[0]
    pos[0][2] = mov[1]

    # morte se ti tocchi la coda
    for i in range(lun):
        if pos[0][1] == pos[i + 1][1] and pos[0][2] == pos[i + 1][2]:
            lun = 1
            print("sei morto")
    scambio()

    # mangi cibo e ti allunghi
    if pos[0][1] == cibo[0] and pos[0][2] == cibo[1]:
        lun += 1
        cibo[0] = randint(1, (xf - lar) / lar) * lar
        cibo[1] = randint(1, (yf - lar) / lar) * lar
        pos.append([lun, int(pos[0][1]), int(pos[0][2])])
        print("punteggio: " + str(lun))

    screen.fill((0, 0, 0))

    # print cubetti e colorazione
    for i in range(lun + 1):
        m = int(255 / lun)
        j = i * m
        pygame.draw.rect(screen, (0, j, 255), pygame.Rect(pos[i][1], pos[i][2], lar, lar))

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(cibo[0], cibo[1], lar, lar))

    pygame.display.flip()
    clock.tick(10)
