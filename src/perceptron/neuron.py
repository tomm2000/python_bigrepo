from Tlib import sign

class neuron :
    def __init__(self, w, lr):
        self.weights = w
        self.weights.append(1)
        self.lr = lr

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
        uess = self.guess(inputs)
        error = target - guess

        for i in range(len(self.weights)):
            self.weights[i] += (error * inputs[i] * self.lr)
            self.weights[i] = round(self.weights[i], 8)