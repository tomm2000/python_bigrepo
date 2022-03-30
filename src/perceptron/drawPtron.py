import pygame

from Tlib import drawCircle
from Tlib import spread
from Tlib import drawLinePoints

# PYGAME: ----------
width = 600
height = 400
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
done = False
# ------------------

# COLORI: ----------
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
red = (255, 0, 0)
green = (0, 255, 0)
# ------------------

# VARIE ------------
inputNodes = 3
hiddenNodes = 5
outputNodes = 2
# ------------------

class node :
    def __init__(self, y, layer):
        self.x = int(width/3) * layer + 100
        self.y = y
        self.layer = layer
    
    def draw(self):
        drawCircle(self.x, self.y, screen, 10, black)


class network :
    def __init__(self, iN, hN, oN):
        self.iNodes = []
        for i in range(iN):
            j = i + 1
            self.iNodes.append(node(spread(j, 0, iN + 1, 0, height), 0))
        
        self.hNodes = []
        for i in range(hN):
            j = i + 1
            self.hNodes.append(node(spread(j, 0, hN + 1, 0, height), 1))

        self.oNodes = []
        for i in range(oN):
            j = i + 1
            self.oNodes.append(node(spread(j, 0, oN + 1, 0, height), 2))

    def drawNodes(self):
        for n in self.iNodes:
            n.draw()
        for n in self.hNodes:
            n.draw()
        for n in self.oNodes:
            n.draw()

    def drawConnections(self):
        for i in self.iNodes:
            for h in self.hNodes:
                drawLinePoints(i.x, i.y, h.x, h.y, screen, gray)
        
        for h in self.hNodes:
            for o in self.oNodes:
                drawLinePoints(h.x, h.y, o.x, o.y, screen, gray)

screen.fill(white)

net = network(inputNodes, hiddenNodes, outputNodes)
net.drawConnections()
net.drawNodes()


pygame.display.flip()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    pygame.display.flip()
    clock.tick(60)