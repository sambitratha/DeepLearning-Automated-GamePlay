import sys
import os
import pygame
import random
from pygame.locals import *
import pygame.locals as locals


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

windowheight = 500
windowlength = 800

upmargin = windowheight / 20


welcomebg = pygame.image.load('assets/welcome.png')
print(welcomebg)

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

            if event.type == KEYDOWN and event.key == K_p:
                return



def maingame():
    #execute this when user starts playing
    ballx = windowlength/4
    bally = (windowheight - upmargin) / 2
    radius = 5
    width = 50
    gap = 20
    screenheight = windowheight - upmargin
    distance = windowlength/2
    pipes = []
    #add two pipes in the start of the game
    pipes.append([windowlength/2,random.randint(10, screenheight - 10)])
    pipes.append([windowlength, random.randint(10, screenheight - 10)])

    velx = -4
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((windowlength, windowheight))
    pygame.display.set_caption("Car Racing")
    while True:
        display.fill(colors['white'])

        pygame.draw.circle(display, colors['red'], (ballx, bally), radius)

        for pipe in pipes:
            pygame.draw.rect(display, colors['black'], (pipe[0], upmargin, width, pipe[1]))
            lpipex = pipe[0]
            lpipey = upmargin + pipe[1] + gap
            lpipewidth = width
            lpipeheight = screenheight - pipe[1] - gap
            pygame.draw.rect(display, colors['black'], (lpipex, lpipey, lpipewidth, lpipeheight))

        for pipe in pipes:
            pipe[0] += velx

        if pipes[-1][0] + distance < windowlength:
            pipes.append([pipes[-1][0] + distance, random.randint(10, screenheight -10)])

        if pipes[0][0] + pipes[0][1] < 0:
            pipes.pop(0)


        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return
            

        pygame.display.update()

    pass

def showGameover():
    #show this screen when the user is done playing the game
    pass



if __name__ == '__main__':
    showWelcomeScreen()
    maingame()
    showGameover()


