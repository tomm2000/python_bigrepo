from Tlib import sign

# COLORI: ----------
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
red = (255, 0, 0)
green = (0, 255, 0)
# ------------------

class perceptron :
    def __init__(self, w, lr, screen):
        self.weights = w
        self.lr = lr
        self.canvas = screen

    def guess(self, inputs):
        output = 0
        for i in range(len(self.weights)):
            output += self.weights[i] * inputs[i]
        
        return sign(output)

    def printWeights(self):
        for i in range(len(self.weights)):
            print("weight #" + str(i) + " -> " + str(self.weights[i]))
        print("=======================")

    def train(self, inputs, target):
        guess = self.guess(inputs)
        error = target - guess

        for i in range(len(self.weights)):
            self.weights[i] += (error * inputs[i] * self.lr)
            self.weights[i] = round(self.weights[i], 8)