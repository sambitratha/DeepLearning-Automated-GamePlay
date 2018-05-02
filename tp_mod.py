import sys
import numpy
import csv
import math
import os
import random
import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from torch.autograd import Variable
import pickle



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





class DQN(nn.Module):
    def __init__(self, dimension = 4):
        super(DQN, self).__init__()
        self.dimension = dimension
        self.dim1 = 20
        self.dim2 = 30
        self.fc1 = nn.Linear(4, self.dim1)
        self.fc1.weight = nn.Parameter(nn.init.xavier_normal(torch.Tensor(self.dim1, 4)))
        self.fc2 = nn.Linear(self.dim1 , self.dim2)
        self.fc2.weight = nn.Parameter(nn.init.xavier_normal(torch.Tensor(self.dim2, self.dim1)))
        self.fc3 = nn.Linear(self.dim2, 1)

    def forward(self, x):
        print self.fc1.weight
        # print x
        layer1 = self.fc1(x)
        # print "finished"
        layer2 = self.fc2(layer1)
        layer2 = F.dropout(layer2)
        output = self.fc3(layer2)
        return output


class DQNmodel:
    def __init__(self, episilion = 0.99, decay = 0.995, discount = 0.9, learning_rate = 0.01):
        self.episilion = episilion
        self.decay = decay
        self.discount = discount
        self.learning_rate = learning_rate
        self.model = DQN()
        self.optimizer = torch.optim.SGD(self.model.parameters(),lr = self.learning_rate)

    def getAction(self, state):

        random_val = float(random.randint(1, 100))/100
        if random_val < self.episilion:
            return random.randint(1, 5) % 2

        (vel, h_dist, v_dist) = state
        state1 = [vel, h_dist, v_dist, 0]
        state2 = [vel, h_dist, v_dist, 1]

        state1 = Variable(torch.from_numpy(np.array(state1))).float()
        state2 = Variable(torch.from_numpy(np.array(state2))).float()

        out1 = self.model(state1)
        out2 = self.model(state2)

        print "out1 = " , out1
        print "out2 = " , out2 
        # if np.array(out1)[0] > np.array(out2)[0]:
        #     return 0
        # else:
        #     return 1

        return 1

    def updateQValue(self, current_state, next_state, reward):
        cur_state = [current_state[i] for i in range(len(current_state))]
        inp = Variable(torch.from_numpy(np.array(cur_state))).float()
        output = self.model(inp)

        state1 = [next_state[i] for i in range(len(next_state))] + [0]
        state2 = state1[:-1] + [1]

        state1 = Variable(torch.from_numpy(np.array(state1))).float()
        state2 = Variable(torch.from_numpy(np.array(state2))).float()

        out1 = self.model(state1)
        out2 = self.model(state2)

        # print "out1 = " , out1
        # print "out2 = " , out2         

        maxim = int(out1[0])
        # print "maxim = " , maxim

        if int(out1[0]) < int(out2[0]):
            maxim = int(out2[0])

        test_label = Variable(torch.from_numpy(np.array([maxim * self.discount + reward]))).float()

        loss = F.smooth_l1_loss(output.view(-1), test_label)

        self.optimizer.zero_grad()
        loss.backward()

        self.optimizer.step()


    def update_epsilion(self):
        self.episilion = self.episilion * (self.decay)

    def writeQTable(self):
        modelobject = open("modeldump", 'wb')
        pickle.dump(self.model, modelobject)

    def readQTable(self):
        modelobject = open("modeldump", 'r')
        self.model = pickle.load(modelobject)


    def experience_replay(self, memory):
        for curr_mem in memory:
            [curr_state, next_state, reward] = curr_mem
            self.updateQValue(curr_state, next_state, reward)
        

if __name__ == '__main__':
    model = DQNmodel()

model.updateQValue((-10, 2, 3, 4), (1, 2, 3), 100)
