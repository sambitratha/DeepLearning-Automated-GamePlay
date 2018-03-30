import sys
import os
import pygame
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
    display = pygame.display.set_mode((800, 600))
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
    pass

def showGameover():
    #show this screen when the user is done playing the game
    pass



if __name__ == '__main__':
    showWelcomeScreen()
    maingame()
    showGameover()


