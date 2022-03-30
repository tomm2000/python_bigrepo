import pygame
from pygame import gfxdraw as gfx
from random import randint
pygame.init()
pygame.font.init()

# dimensioni
lung = 1000
alt = 600
ris = 10
l = int(lung / ris)
a = int(alt / ris)
lung = l * ris
alt = a * ris

# font
font = pygame.font.SysFont("Calibri", ris + 3)

# variabili di ciclo & pygame
clock = pygame.time.Clock()
screen = pygame.display.set_mode((lung, alt))
done = False
still_iterating = True

# variabili incremento
timer = 0
contatore = 0

# colori
Nero = (0, 0, 0)
Rosso = (255, 0, 0)

# variabili sopravvivenza
starve = 11
birth = 5
lonely = 3
percent = 48 # su 100
plus = 6

# variabili velocità e iterazioni
iterazioni = 0
tick = 60

# iniziallizzazione array & matrici
riga = []
matrice = []
matricecheck = []

# creazione random matrice di base
for i in range(l):
    riga = []
    for j in range(a):
        if i == 0 or i == l - 1 or j == 0 or j == a - 1:
            riga.append(1)
        else:
            random = randint(0, 99)
            if random < percent:
                riga.append(1)
            else:
                riga.append(0)
    matrice.append(riga)


def drawrect(spigolo, lunghezza, altezza, color):
    pygame.draw.rect(screen, color, pygame.Rect(spigolo[0], spigolo[1], lunghezza, altezza))


# 1= |/
# 2= \|
# 3= /|
# 4= |\
# 5= ||

def drawtriangle(x, y, type):
    v1 = (x * ris, y * ris)
    v2 = (x * ris + ris - 1, y * ris)
    v3 = (x * ris + ris - 1, y * ris + ris - 1)
    v4 = (x * ris, y * ris + ris - 1)

    if type == 1:
        gfx.filled_polygon(screen, (v1, v2, v4), Nero)
    elif type == 2:
        gfx.filled_polygon(screen, (v1, v2, v3), Nero)
    elif type == 3:
        gfx.filled_polygon(screen, (v2, v3, v4), Nero)
    elif type == 4:
        gfx.filled_polygon(screen, (v1, v3, v4), Nero)


def smooth(mat, x, y):
    if (mat[x][y + 1] == 0 and mat[x][y - 1] == 1) and (mat[x + 1][y] == 0 and mat[x - 1][y] == 1):
        drawtriangle(x, y, 1)

    elif (mat[x][y + 1] == 0 and mat[x][y - 1] == 1) and (mat[x + 1][y] == 1 and mat[x - 1][y] == 0):
        drawtriangle(x, y, 2)

    elif (mat[x][y + 1] == 1 and mat[x][y - 1] == 0) and (mat[x + 1][y] == 1 and mat[x - 1][y] == 0):
        drawtriangle(x, y, 3)

    elif (mat[x][y + 1] == 1 and mat[x][y - 1] == 0) and (mat[x + 1][y] == 0 and mat[x - 1][y] == 1):
        drawtriangle(x, y, 4)

    elif mat[x][y] == 1:
        drawrect((x * ris, y * ris), ris, ris, Nero)


def contovicini(mat, x, y):
    contatore = 0
    for n in [-1, 0, 1]:
        for m in [-1, 0, 1]:
            if mat[x + n][y + m] == 1:
                contatore += 1
    if mat[x][y] == 1:
        contatore -= 1

    return contatore


def contoviciniplus(mat, x, y):
    contatore = 0
    if (x in [0, 1, l - 1, l -2]) or (y in [0, 1, a - 1, a -2]):
        contatore = 25
    else:
        for n in [-2, -1, 0, 1, 2]:
            for m in [-2, -1, 0, 1, 2]:
                if mat[x + n][y + m] == 1:
                    contatore += 1
        if mat[x][y] == 1:
            contatore -= 1

    return contatore


def iterazione(matIn):
    matricetemp = []
    for i in range(l):
        riga = []
        for j in range(a):
            if i == 0 or i == l - 1 or j == 0 or j == a - 1:
                riga.append(1)
            else:
                if contoviciniplus(matIn, i, j) <= plus:
                    riga.append(0)
                elif contovicini(matIn, i, j) >= starve:
                    riga.append(0)
                elif contovicini(matIn, i, j) >= birth:
                    riga.append(1)
                elif contovicini(matIn, i, j) <= lonely:
                    riga.append(0)
                elif matIn[i][j] == 1:
                    riga.append(1)
                else:
                    riga.append(0)
        matricetemp.append(riga)
    matIn = matricetemp
    return matIn


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((128, 128, 128))

    for i in range(l):
        for j in range(a):
            if i == 0 or i == l - 1 or j == 0 or j == a - 1:
                drawrect((i * ris, j * ris), ris, ris, Nero)

    for i in range(l - 2):
        for j in range(a - 2):
            if matrice[i + 1][j + 1] == 1:
                smooth(matrice, i + 1, j + 1)

    timer += 1
    if timer >= int(tick / 3) and still_iterating:
        matricecheck = matrice.copy()
        matrice = iterazione(matrice)
        if matrice == matricecheck:
            still_iterating = False
        else:
            iterazioni += 1
            timer = 0

    if still_iterating:
        screen.blit(font.render("Iterazione: " + str(iterazioni), True, (255, 0, 0)), (5, 0))
    else:
        screen.blit(font.render("Done in: " + str(iterazioni) + " iterations", True, (0, 255, 0)), (5, 0))

    pygame.display.flip()
    clock.tick(tick)
