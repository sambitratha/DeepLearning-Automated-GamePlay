import sys
import os
import random
import math
import pygame
from pprint import  pprint
from pygame.locals import *
import pygame.locals as locals
import threading
import time

windowwidth = 300
windowheight = 300
boxwidth = 50
boxheight = 50
margin = 15
gap = 5

pygame.init()


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (127, 127, 127)


board = []
rows = 5
cols = 5
for i in range(rows):
    board.append([0] * 5)

l = range(0, rows * cols)
random.shuffle(l)

obstacles = l[:4]



for obstacle in obstacles:
    if obstacle != 24:
        row = obstacle / cols
        col = obstacle - (row * cols)
        board[row][col] = 1

pprint(board)
board[4][4] = 2
qvalues = {}

def init():
    global qvalues
    for r in range(5):
        for c in range(5):
            for a in range(4):
                random_val = float(random.randint(0, 100)) / 100
                if random.randint(0, 5) % 2 == 1:
                    random_val *= -1

                qvalues[(r, c, a)] = random_val

    return

x = 0
y = 0
def train(episodes, episilion, learning_rate, discount):
    global x, y
    print "started training" + str(episodes)
    for episode in range(episodes):
        curpos = [0, 0]
        x = 0
        y = 0
        oldposx = curpos[0]
        oldposy = curpos[1]
        counter = 0
        while True:
            time.sleep(0.1)
            counter += 1
            randomnumber = float(random.randint(0, 100)) / 100
            action = 0
            if randomnumber > episilion:
                for a in range(1, 4):
                    if qvalues[(curpos[0], curpos[1], a)] > qvalues[(curpos[0], curpos[1], action)]:
                        action = a
            else:
                action = random.randint(0, 3)

            reward = 0
            if action == 0:
                if curpos[0] == 4:
                    reward = 0
                else:
                    curpos[0] += 1


            elif action == 1:
                if curpos[1] == 0:
                    reward = 0
                else:
                    curpos[1] -= 1

            elif action == 2:
                if curpos[0] == 0:
                    reward = 0
                else:
                    curpos[0] -= 1
            else:
                if curpos[1] == 4:
                    reward = 0
                else:
                    curpos[1] += 1

            if board[curpos[0]][curpos[1]] == 2:
                reward = 1000000
            elif board[curpos[0]][curpos[1]] == 1:
                reward = -100000
            else:
                reward = -1

            max_val = qvalues[(curpos[0], curpos[1], 0)]
            for a in range(1, 4):
                if qvalues[(curpos[0], curpos[1], a)] > max_val:
                    max_val = qvalues[(curpos[0], curpos[1], a)]

            qvalues[(oldposx, oldposy , action)] += learning_rate * (reward + discount * max_val - qvalues[(oldposx, oldposy, action)])

            oldposx = curpos[0]
            oldposy = curpos[1]
            x = curpos[0]
            y = curpos[1]
            #print (curpos[0], curpos[1])
            if reward < -1:
                print("episode ", episode, ": failed")
                break
            if curpos[0] == 4 and curpos[1] == 4:
                print("episode ", episode, ": won in ", counter, "moves")
                break

            episilion -= float(1)/episodes


def window():
    display = pygame.display.set_mode((windowwidth, windowheight))
    pygame.display.set_caption("AI")
    while True:
        display.fill(white)

        for r in range(5):
            for c in range(5):
                color = grey
                if board[r][c] == 2:
                    color = green
                if board[r][c] == 1:
                    color = black
                cordx = margin + c * (boxwidth + gap)
                cordy = margin + r * (boxheight + gap)
                pygame.draw.rect(display, color, (cordx , cordy, boxwidth, boxheight) )

        pygame.draw.circle(display, blue, (margin + y * (boxwidth + gap) + boxwidth/2 , margin + x * (boxheight + gap) + boxheight/2), 10)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        pygame.display.update()


class mythread(threading.Thread):
    def __init__(self, flag):
        threading.Thread.__init__(self)
        self.flag = flag

    def run(self):
        if self.flag:
            train(40, 0.9, 0.2, 0.9)
        else:
            window()



init()
#thread.start_new_thread(train, (100, 0.9, 0.2, 0.9))
#thread.start_new_thread(window, ())

thread1 = mythread(True)
thread2 = mythread(False)

thread1.start()
thread2.start()




