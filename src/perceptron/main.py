import pygame
from Tlib import drawLinePoints
from Tlib import drawLineFunc
from Tlib import drawCircle
from Tlib import drawCircleOutline
from random import randint

from point import point
from perceptron import perceptron

# PYGAME: ----------
width = 700
height = 700
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
n = 3000
globalLr = 0.0001
size = 3
m = 3
b = 0
# ------------------

points = []
for i in range(n):
    points.append(point(randint(0, width), randint(0, height), size, m, b))

brain = perceptron([randint(-100, 100) / 100, randint(-100, 100) / 100, randint(-100, 100) / 100], globalLr, screen)

screen.fill(white)
#drawLinePoints(0, 0, width, height / m, screen, black)
drawLineFunc(m, b, width, screen, black)

#for pt in points:
#    pt.draw(screen)


pygame.display.flip()
brain.printWeights()



c = 0
itera = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if c == 1 and (itera < len(points)):
        screen.fill(white)
        drawLineFunc(m, b, width, screen, black)

        brain.train([points[itera].x, points[itera].y, points[itera].bias], points[itera].label)
        
        print("iterazione: " + str(itera))

        brain.printWeights()

        for pt in points:
            pt.draw(screen)
            
            if brain.guess([pt.x, pt.y, pt.bias]) == pt.label:
                drawCircleOutline(pt.x, pt.y, screen, 3, green)
            else:
                drawCircleOutline(pt.x, pt.y, screen, 3, red)

        itera += 1

        c = 0
    c += 1
    
    
    pygame.display.flip()
    clock.tick(60)