import sys
import os
import pygame
import random
from pygame.locals import *
import pygame.locals as locals



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


welcomebg = pygame.image.load('assets/welcome.png')
print(welcomebg)

#########################################################################################
def showWelcomeScreen():
    #show this screen when the user first starts the program
    display = pygame.display.set_mode((windowlength, windowheight))
    pygame.display.set_caption("Car Racing")
    print(welcomebg.get_rect())
    while True:
        #display.fill(colors['white'])
        display.blit(welcomebg, welcomebg.get_rect())
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
    pipeimage = pygame.image.load("assets/brick4.png")
    ballx = windowlength/4
    bally = (windowheight - upmargin) / 2
    radius = 15
    width =80
    gap = 100
    screenheight = windowheight - upmargin
    distance = windowlength/2
    pipes = []
    #add two pipes in the start of the game
    pipes.append([windowlength/2,random.randint(50, screenheight - 50)])
    pipes.append([windowlength, random.randint(50, screenheight - 50)])

    vely = 10
    velx = -10
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((windowlength, windowheight))
    pygame.display.set_caption("Car Racing")
    up = False



    while True:
        display.fill(colors['blue'])

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
            pipes.append([pipes[-1][0] + distance, random.randint(50, screenheight - 150)])


        #pop first pipe if needed
        if pipes[0][0] + pipes[0][1] < 0:
            pipes.pop(0)


        clock.tick(30)


        #event call back method
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return

            #if player moved up then set the boolean field to true
            if event.type == KEYDOWN and event.key == K_UP:
                up = True

        #if player pressed up then accelerate the ball upward
        if up:
            vely = -10
            up = False

        #slowly reduce speed of the ball
        if vely < 10:
            vely += 1

        #update the position of ball
        bally += vely


        pygame.draw.rect(display, (50, 50, 70, 100), (0, 0, windowlength, upmargin))
        pygame.display.update()

    pass

def showGameover():
    #show this screen when the user is done playing the game
    pass



if __name__ == '__main__':
    showWelcomeScreen()
    maingame()
    showGameover()


