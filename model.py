import sys
import numpy
import csv
import math
import os
import random





class QLearning:
    def __init__(self,dimension, episilion = 0.99, learning_rate = 0.2, discount = 0.9, decay = 0.995):
        self.dimension = dimension
        self.episilion = episilion
        self.learning_rate = learning_rate
        self.discount = discount
        self.decay = decay
        self.QTable = {}
        self.readQTable()
        pass

    def readQTable(self):
        if not os.path.exists("model.csv"):
            for i in range(self.dimension[0]):
                for j in range(self.dimension[1]):
                    for k in range(self.dimension[2]):
                        self.QTable[(i - 10, j , k - 30, 0)] = 0
                        self.QTable[(i - 10, j , k - 30, 1)] = 0
            return

        with open("model.csv", 'rb') as modelfile:
            csvreader = csv.reader(modelfile, delimiter = ' ')
            for row in csvreader:
                tupl = (int(row[0]), int(row[1]), int(row[2]), int(row[3]))
                self.QTable[tupl] = float(row[4])

    def getAction(self, state):
        (a, b, c) = state
        random_val = float(random.randint(1, 100))/100
        if random_val > self.episilion:
            action = 0
            if self.QTable[(a, b, c, 1)] > self.QTable[(a, b, c, 0)]:
                return 1
            else:
                return 0
        else:
            return random.randint(1, 5) % 2


    def writeQTable(self):

        with open("model.csv", 'wb') as modelfile:
            csvwriter = csv.writer(modelfile, delimiter = ' ')
            for i in range(self.dimension[0]):
                for j in range(self.dimension[1]):
                    for k in range(self.dimension[2]):
                        csvwriter.writerow([str(i - 10) , str(j), str(k - 30), 0, str(self.QTable[(i - 10, j, k - 30, 0)])])
                        csvwriter.writerow([str(i - 10) , str(j), str(k - 30), 1, str(self.QTable[(i - 10, j, k - 30, 1)])])



    def updateQValue(self, current_state, next_state, reward):

        (a, b, c) = next_state
        state1 = (a, b, c, 0)
        state2 = (a, b, c, 1)
        maxim = max(self.QTable[state1], self.QTable[state2])
        self.QTable[current_state] += self.learning_rate * (reward + self.discount * maxim - self.QTable[current_state])

    def update_epsilion(self):
        self.episilion = self.episilion * (self.decay)






