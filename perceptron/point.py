from Tlib import drawCircle

# COLORI: ----------
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)
gray = (190, 190, 190)
red = (255, 0, 0)
green = (0, 255, 0)
# ------------------

class point :
    def __init__(self, x, y, size, m, b):
        self.x = x
        self.y = y
        self.bias = 1
        self.size = size
        
        if y > (m * x) + b:
            self.label = 1
        else:
            self.label = -1
    
    def draw(self, screen):
        if self.label == 1:
            drawCircle(self.x, self.y, screen, self.size, black)
        else:
            drawCircle(self.x, self.y, screen, self.size, black)
    
    def outInfo(self):
        print("x: " + str(self.x) + " -y: " + str(self.y))