import pygame
from random import randint as randint
from math import sqrt as radice


def ran(n, start1, stop1, start2, stop2):
    return int(((n-start1)/(stop1-start1))*(stop2-start2)+start2)


def perc(percentuale, percentualetot):
    if randint(0, percentualetot) > percentuale:
        return False
    else:
        return True


def pixely(ycart):
    return ran(ycart, (yf / 2), -(yf / 2), 0, yf)


def pixelx(xcart):
    return ran(xcart, -(xf / 2), (xf / 2), 0, xf)


def casuale(partenza, fine):
    return randint(0, fine - partenza) - ((fine - partenza) - fine)


xf = 600
yf = 950
lungPerc = 5000
alb = 20
tick = 60
mod = 60 / tick
velsalita = 2 * mod
vellaterale = 2 * mod
accel = 0.1 * (mod ** 2)

pygame.init()
screen = pygame.display.set_mode((xf, yf))
clock = pygame.time.Clock()
done = False

palle = [0]
alberi = []
scie = []
traguardi = [0]


class Traguardo:
    def __init__(self):
        self.posy = -lungPerc
        self.posx = 0

    def movimento(self):
        self.posy += velsalita

    def draw(self):
        pygame.draw.line(screen, (255, 0, 0), (pixelx(-xf / 2), pixely(self.posy)),
                         (pixelx(xf / 2), pixely(self.posy)), 3)


class Scia:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def movimento(self):
        if self.posy < ((yf / 2) + 100):
            self.posy += velsalita

    def draw(self):
        if self.posy < ((yf / 2) + 30):
            pygame.draw.circle(screen, (0, 128, 128), (pixelx(int(self.posx)), pixely(int(self.posy))), 3)


class Albero:
    def __init__(self, sez):
        self.posx = casuale(-(xf / 2), xf / 2)
        self.posy = casuale(-sez * 100, (-sez * 100) + 100)
        self.dist = int(radice(((palle[0].posx - self.posx) ** 2) + ((palle[0].posy - self.posy) ** 2)))
        self.color = (0, 255, 0)

    def movimento(self):
        if self.posy < ((yf / 2) + 100):
            self.posy += velsalita

    def tronco(self):
        if ((-yf / 2) - 30) < self.posy < ((yf / 2) + 30):
            pygame.draw.line(screen, (0, 0, 0), (pixelx(self.posx), pixely(self.posy) - 7),
                             (pixelx(self.posx), pixely(self.posy) + 7), 4)

    def chioma(self):
        if ((-yf / 2) - 30) < self.posy < ((yf / 2) + 30):
            pygame.draw.circle(screen, self.color, (pixelx(self.posx), pixely(self.posy + 7)), 8)

    def distanza(self):
        if 290 < self.posy < 310:
            self.dist = radice(((palle[0].posx - self.posx) ** 2) + ((palle[0].posy - self.posy + 7) ** 2))
            if self.dist <= 6:
                self.color = (255, 0, 0)


class Palla:
    def __init__(self):
        self.posx = 0
        self.posy = 300
        self.direz = 1
        self.vel = 3

    def movimento(self):
        if self.direz == 1:
            if self.vel < vellaterale:
                self.vel += accel
            else:
                self.vel = vellaterale
        elif self.direz == -1:
            if self.vel > -vellaterale:
                self.vel -= accel
            else:
                self.vel = -vellaterale
        self.posx += self.vel
        scie.append(Scia(self.posx, self.posy))

    def draw(self):
        pygame.draw.circle(screen, (100, 100, 100), (pixelx(int(self.posx)), pixely(int(self.posy))), 8)


traguardi[0] = Traguardo()
palle[0] = Palla()
for i in range(int(lungPerc / 100)):
    for j in range(alb):
        alberi.append(Albero(i))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE]:
            palle[0].direz = palle[0].direz * -1

    screen.fill((255, 255, 255))

    traguardi[0].movimento()
    traguardi[0].draw()

    for i in range(len(scie)):
        scie[i].movimento()
        scie[i].draw()

    palle[0].movimento()
    palle[0].draw()

    for i in range(len(alberi)):
        alberi[i].movimento()
        alberi[i].tronco()
        alberi[i].distanza()
    for i in range(len(alberi)):
        alberi[i].chioma()

    pygame.display.flip()
    clock.tick(tick)
