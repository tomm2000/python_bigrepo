import pygame
from random import randint as rand
from math import sqrt as sqrt


def ran(n, start1, stop1, start2, stop2):
    return int(((n-start1)/(stop1-start1))*(stop2-start2)+start2)


def distanza(x1, x2, y1, y2):  # calcola la distanza fra due punti
    return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))


xf = 1000  # larghezza finestra
yf = 800  # altezza finestra
done = False

tick = 0  # tempo passato
g = 3  # velocità di caduta
a = 0.9  # rallentamento attrito dell'aria
vita = 300  # tempo di vita
gen = 0  # generazione
pop = 200  # popolazione (numero di sassi alla volta)
sassi = []  # array che contiene gli oggetti "Sasso"
sassit = []  # array temporaneo
bersagli = [0]  # array che contiene gli oggetti "Bersaglio"
ostacoli = [0, 0, 0, 0, 0, 0]  # array che contiene gli oggetti "Ostacolo"
pool = []  # pool riproduzione
allfit = []  # array che contiene tutte le fitness
conto = 0  # contatore di quanti sassi hanno colpito il bersaglio


class Ostacolo:  # Definisce le proprietà degli oggetti "Ostacolo"
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):  # disegna l'oggetto
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x1, self.y1, self.x2-self.x1, abs(self.y2-self.y1)))


class Bersaglio:  # Definisce le proprietà degli oggetti "Bersaglio"
    def __init__(self, posx, posy, r, colore):
        self.posx = posx
        self.posy = posy
        self.r = r
        self.colore = colore

    def draw(self):  # disegna l'oggetto
        pygame.draw.circle(screen, self.colore, (self.posx, self.posy), self.r, self.r)


class Sasso:  # Definisce le proprietà degli oggetti "Sasso"
    def __init__(self):
        self.posx = xf / 2
        self.posy = 0
        self.vel = 0
        self.mod = 0
        self.dna = []
        self.muro = False
        self.ttocco = vita
        if gen == 0:  # creazione iniziale
            for k in range(vita):
                self.dna.append((rand(0, 30) - 15) / 5)
        else:  # riproduzione
            genitore = pool[rand(0, len(pool) - 1)]
            p = rand(1, 10)
            if p <= 9:  # il 90% sono generati da un genitore
                for l in range(vita):
                    if l > (sassi[genitore].ttocco - 50):
                        self.dna.append((rand(0, 16) - 8) / 5)
                    else:
                        self.dna.append(sassi[genitore].dna[l] + ((rand(0, 2) - 1) / 5))
            else:  # il restante 10% sono generati random
                for l in range(vita):
                    self.dna.append((rand(0, 30) - 15) / 5)

    def fisica(self):  # gestisce la fisica degli oggetti "Sasso"
        # i prossimi 6 if / elif controllano le collisioni con gli ostacoli
            if (ostacoli[0].x2 > self.posx > ostacoli[0].x1) and (ostacoli[0].y2 > self.posy > ostacoli[0].y1):
                self.mod = round(2 / 10, 3)
                if not self.muro:
                    self.muro = True
                    self.ttocco = tick
            elif (ostacoli[1].x2 > self.posx > ostacoli[1].x1) and (ostacoli[1].y2 > self.posy > ostacoli[1].y1):
                self.mod = round(2 / 10, 3)
                if not self.muro:
                    self.muro = True
                    self.ttocco = tick
            elif (ostacoli[2].x2 > self.posx > ostacoli[2].x1) and (ostacoli[2].y2 > self.posy > ostacoli[2].y1):
                self.mod = round(3 / 10, 3)
                if not self.muro:
                    self.muro = True
                    self.ttocco = tick
            elif (ostacoli[3].x2 > self.posx > ostacoli[3].x1) and (ostacoli[3].y2 > self.posy > ostacoli[3].y1):
                self.mod = round(4 / 10, 3)
                if not self.muro:
                    self.muro = True
                    self.ttocco = tick
            elif (ostacoli[4].x2 > self.posx > ostacoli[4].x1) and (ostacoli[4].y2 > self.posy > ostacoli[4].y1):
                self.mod = round(7 / 10, 3)
                if not self.muro:
                    self.muro = True
                    self.ttocco = tick
            elif (ostacoli[5].x2 > self.posx > ostacoli[5].x1) and (ostacoli[5].y2 > self.posy > ostacoli[5].y1):
                self.mod = round(7 / 10, 3)
                if not self.muro:
                    self.muro = True
                    self.ttocco = tick
            elif distanza(self.posx, bersagli[0].posx, self.posy, bersagli[0].posy) > bersagli[0].r:  # controlla la
                # collisione col bersaglio
                self.vel += self.dna[tick]
                self.vel = self.vel * a
                if self.vel > 20:  # limite velocità
                    self.vel = 20
                if self.posx > xf:  # limite muro dx
                    self.posx = xf - 2
                elif self.posx < 0:  # limite muro sx
                    self.posx = 2
                elif not self.posy >= (yf - 2):  # movimento laterale
                    self.posx += int(self.vel)
                if self.posy >= (yf - 2):  # limite pavimento
                    self.posy = yf - 2
                    self.mod = 1.75
                    if not self.muro:
                        self.muro = True
                        self.ttocco = tick
                else:
                    self.posy += g
            else:
                self.mod = 4

    def fitness(self):  # calcola la fitness di ogni oggetto "Sasso"
        dist = distanza(self.posx, bersagli[0].posx, self.posy, bersagli[0].posy)  # fitn. in bassa alla dist. dal bers.
        if dist < bersagli[0].r:
            dist = bersagli[0].r
        self.fit = ran(dist, bersagli[0].r, 600, 100, 0)
        self.fit = int(self.fit * self.mod)  # fitness in base ad altri modificatori
        if self.fit < 1:
            self.fit = 1
        allfit.append(self.fit)

    def draw(self):  # disegna l'oggetto
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.posx - 2, self.posy - 2, 4, 4))

    fit = 0


pygame.init()  # cose pygame
screen = pygame.display.set_mode((xf, yf))  # cose pygame
clock = pygame.time.Clock()  # cose pygame

for i in range(pop):  # crea gli oggetti "Sasso" per la prima volta
    sassi.append(i)
    sassi[i] = Sasso()

bersagli[0] = Bersaglio(int(xf / 2), yf - 20, 20, (255, 0, 0))  # definisce il bersaglio
ostacoli[2] = Ostacolo(0, 350, 600, 370)  # definisce il ostacolo medio
ostacoli[3] = Ostacolo(550, 450, 1000, 470)  # definisce l'ostacolo basso
ostacoli[0] = Ostacolo(0, 250, 400, 270)  # definisce l'ostacolo doppio 1
ostacoli[1] = Ostacolo(600, 250, 1000, 270)  # definisce l'ostacolo doppio 2
ostacoli[4] = Ostacolo(550, 470, 570, 550)  # definisce l'ostacolo basso +
ostacoli[5] = Ostacolo(420, 370, 440, 550)  # definisce l'ostacolo basso +2

print("-----------------------")

while not done:  # GAME CYCLE
    for event in pygame.event.get():  # cose pygame
        if event.type == pygame.QUIT:  # cose pygame
            done = True  # cose pygame
    screen.fill((128, 128, 128))  # cose pygame
    bersagli[0].draw()  # avvia il disegno del bersaglio
    for i in range(len(ostacoli)):  # avvia il disegno degli ostacoli
        ostacoli[i].draw()

    for i in range(pop):    # avvia il disegno degli sassi
        sassi[i].fisica()
        sassi[i].draw()

    tick += 1  # avanza il tempo
    if tick >= vita:
        conto = 0
        allfit = []
        tick = 0
        gen += 1
        pool = []
        for i in range(pop):  # ogni tot tick si crea una nuova generazione di sassi
            sassi[i].fitness()
            for j in range(sassi[i].fit):  # genera la pool di riproduzione
                pool.append(i)
            sassit.append(Sasso())
        sassi = sassit
        sassit = []
        print("Generazione: " + str(gen))  # questo e le prossime 7 righe sono solo di output per il controllo
        print("Maxfit: " + str(max(allfit)) + " / 400")
        for i in range(len(allfit)):
            if allfit[i] == 400:
                conto += 1
        print("Bersaglio colpito: " + str(conto) + " volte")
        print("Il " + str(round(((conto * 100) / 400), 2)) + "% hanno colpito")
        print("-----------------------")

    pygame.display.flip()  # cose pygame
    clock.tick(60)  # quante operazioni sono svolte al secondo
