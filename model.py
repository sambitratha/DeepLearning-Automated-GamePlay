import sys
import os
import pygame
import random
from pygame.locals import *
from  math import  cos, sin, pi
import pygame.locals as locals
import model
import time



##########################################################################################

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (127, 127, 127)

colors = {}
colorlist = ['black', 'white', 'red' , 'green' , 'blue' , 'grey' ]
colors['black']     = black
colors['white']     = white
colors['red']       = red
colors['green']     = green
colors['blue']      = blue
colors['grey']      = grey
##########################################################################################

windowheight = 500
windowlength = 800

upmargin = windowheight / 20

font = None

memory = None

welcomebg = pygame.image.load('assets/welcome2.jpg')
print(welcomebg)

# Qmodel = model.QLearning([30, 40, 60], episilion=0.999)
Qmodel = model.DQN()

#########################################################################################
def showWelcomeScreen():
    #show this screen when the user first starts the program
    display = pygame.display.set_mode((windowlength, windowheight))
    pygame.display.set_caption("Car Racing")
    print(welcomebg.get_rect())
    while True:
        #display.fill(colors['white'])
        cropRect = (0, 0, windowlength, windowheight)
        display.blit(welcomebg, dest = (0, 0), area= cropRect)
        #display.blit(welcomebg, welcomebg.get_rect())

        tObject, tRect = getStringObject("Press 'P' to Play", windowlength/2 , 430)
        display.blit(tObject, tRect)
        display.set_alpha(255)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if (event.type == KEYDOWN or event.type == KEYUP) and event.key == K_p:
                return

#########################################################################################

def maingame():
    #execute this when user starts playing

    global memory

    memory = []

    playerscore = 0
    pipeimage = pygame.image.load("assets/brick4.png")
    ballx = windowlength/4
    bally = (windowheight - upmargin) / 2
    radius = 15
    width = 80
    gap = 100
    screenheight = windowheight - upmargin
    distance = windowlength/2
    pipes = []
    #add two pipes in the start of the game
    height1 = random.randint(200, 300)
    height2 = random.randint(200, 300)
    pipes.append([windowlength/2, height1])
    pipes.append([windowlength, height2])


    crossedPole = False

    playerUpAccl = -10
    playerMaxVel = 10
    playerAccl = 1
    vely = 10
    velx = -10
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((windowlength, windowheight))
    pygame.display.set_caption("Car Racing")
    up = False
    flag = False

    lastaction = None
    prevstate = None
    curstate = None
    reward = None

    gameover = False

    pixel_batch = 20

    while True:
        display.fill(colors['blue'])

        curvel = vely
        horizontal_distance = 0
        vertical_distance = 0
        if ballx > pipes[0][0] + width/2:
            horizontal_distance = (pipes[1][0] - ballx)
            vertical_distance = pipes[1][1] - bally
        else:
            horizontal_distance = pipes[0][0] + width/2 - ballx
            vertical_distance = pipes[0][1] - bally

        horizontal_distance /= pixel_batch
        vertical_distance  /= pixel_batch

        horizontal_distance = max(horizontal_distance, 0)


        curstate = (curvel, horizontal_distance, vertical_distance)


        if lastaction != None:
            # Qmodel.updateQValue(prevstate, curstate, reward)
            # Qmodel.update_epsilion()
            memory.append([prevstate, curstate, reward])



        if gameover:
            # Qmodel.writeQTable()
            return playerscore

        lastaction = Qmodel.getAction(curstate)

        if lastaction == 1:
            up = True
            vely = playerUpAccl




        pygame.draw.circle(display, colors['red'], (ballx, bally), radius)



        for pipe in pipes:
            #pygame.draw.rect(display, colors['black'], (pipe[0], upmargin, width, pipe[1]))
            cropRect = (0, 100, width, pipe[1])
            display.blit(pipeimage, dest = (pipe[0], upmargin), area= cropRect)
            lpipex = pipe[0]
            lpipey = upmargin + pipe[1] + gap
            lpipewidth = width
            lpipeheight = screenheight - pipe[1] - gap
            cropRect = (0, 100, lpipewidth, lpipeheight)
            #pygame.draw.rect(display, colors['black'], (lpipex, lpipey, lpipewidth, lpipeheight))
            display.blit(pipeimage, dest = (lpipex, lpipey), area = cropRect)

        #move pipes to left
        for pipe in pipes:
            pipe[0] += velx

        #add new pipe to list
        if pipes[-1][0] + distance < windowlength:
            #pipes.append([pipes[-1][0] + distance, random.randint(50, screenheight - 200)])
            newheight = random.randint(150, 350)
            #print "newheight : ", newheight
            pipes.append([pipes[-1][0] + distance, newheight])
            #print pipes




        clock.tick(150)


        #event call back method
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return playerscore

            #if player moved up then set the boolean field to true
            # if event.type == KEYDOWN and event.key == K_UP:
            #     up = True
            #     vely = playerUpAccl


        if vely < playerMaxVel and not up:
            vely += playerAccl
        #if player pressed up then accelerate the ball upward
        if up:
            up = False

        #update the position of ball
        # if bally + radius < windowheight :
        #     bally += vely

        if radius + upmargin < bally < windowheight - radius:
        	bally += vely

        # elif radius + upmargin > bally:
        # 	if vely > 0:
        # 		bally += vely

        # elif bally > windowheight - radius:
        # 	if vely < 0:
        # 		bally += vely

        else:
            gameover = True


        if bally + radius >= windowheight:
            vely = int(float(-0.8 * vely))


        curpipe = pipes[0]
        if not crossedPole:
            if ballx > curpipe[0] + width/2 :
                reward = 2
                playerscore += 1
                crossedPole = True

        #pop first pipe if needed
        if pipes[0][0] + pipes[0][1] < 0:
            if  crossedPole:
                crossedPole = False
            pipes.pop(0)


        ball = {'center' : (ballx, bally) , 'radius' : radius}
        for pipe in pipes:
            upipe = {}
            upipe['start'] = [pipe[0], upmargin]
            upipe['width'] = width
            upipe['height'] = pipe[1]
            lpipe = {}
            lpipe['start'] = [pipe[0], upmargin + pipe[1] + gap]
            lpipe['width'] = width
            lpipe['height'] = screenheight - pipe[1] - gap

            if checkForCollision(ball, upipe) or checkForCollision(ball, lpipe):
               gameover = True


        if gameover:
            reward = -100000000
        else:
            if not crossedPole:
                reward = 1




        pygame.draw.rect(display, (50, 50, 70, 100), (0, 0, windowlength, upmargin))

        tObject, tRect = getStringObject(str(playerscore), windowlength/2, 10)
        display.blit(tObject, tRect)


        (a, b, c) = curstate
        prevstate = (a, b, c, lastaction)



        if not flag:
            pygame.display.update()

    pass

def showGameover(score):
    #show this screen when the user is done playing the game

    display = pygame.display.set_mode((windowlength, windowheight))
    pygame.display.set_caption("Game Over")
    gameoverBG = pygame.image.load('assets/gameover.jpg')
    print(welcomebg.get_rect())
    while True:
        #display.fill(colors['white'])
        cropRect = (0, 0, windowlength, windowheight)
        display.blit(gameoverBG, dest = (0, 0), area= cropRect)

        tObject, tRect = getStringObject("Your Score: " + str(score), windowlength/2, 50 , colors['black'])
        display.blit(tObject, tRect)
        #display.blit(welcomebg, welcomebg.get_rect())
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if (event.type == KEYDOWN or event.type == KEYUP) and event.key == K_p:
                return
    pass



def checkForCollision(circle, rect):
    (cx, cy) = circle['center']
    r = circle['radius']
    for degree in range(0, 360, 5):
        theta = float(degree * pi) / 180
        point = [r * cos(theta) + cx, r * sin(theta) + cy]
        if rect['start'][0] < point[0] < rect['start'][0] + rect['width'] and rect['start'][1] < point[1] < rect['start'][1] + rect['height']:
            return True

    return False


def getStringObject(s,centerx,centery, color = colors['white']):

    textObj = font.render(s,True, color )
    #textObj.set_alpha(50)
    textRect = textObj.get_rect()
    textRect.center = (centerx, centery)
    return textObj , textRect



if __name__ == '__main__':
    pygame.init()
    font = pygame.font.Font("assets/EraserRegular.ttf",30)
    start = time.time()
    maxscore = 0
    counter = 0
    while True:
    	
    	counter += 1
        now = time.time()
        if now - start > 60 * 60 * 3:
            break
        #showWelcomeScreen()
        score = maingame()
        maxscore = max(maxscore, score)

        Qmodel.experience_replay(memory)
        print "episode ", counter, " : ", "maxscore = ", maxscore, " score = ", score
#showGameover(score)
