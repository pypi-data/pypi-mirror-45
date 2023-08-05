# =============================================================================
# Title: Connect Four
# Author: Ryan J. Slater
# Date: Wed Nov 14 14:38:45 2018
# =============================================================================

import pygame
import time
import numpy as np


def text_objects(text, font, color=(0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg, loc, size, ic, ac, action=None, param=None, textSize=30):
    x, y = loc
    w, h = size
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        text = pygame.font.SysFont('couriernew', textSize)
        textSurf, textRect = text_objects(msg, text)
        textRect.center = ((x+(w/2)), (y+(h/2)))
        window.blit(textSurf, textRect)
        if click[0] == 1 and action is not None:
            if param is not None:
                action(param)
            else:
                action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))
        text = pygame.font.SysFont('couriernew', textSize)
        textSurf, textRect = text_objects(msg, text)
        textRect.center = ((x+(w/2)), (y+(h/2)))
        window.blit(textSurf, textRect)


class COLORS:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    DARK_RED = (150, 0, 0)


def quitApp():
    pygame.quit()
    quit()


def setPlayerCount(count):
    global numPlayers
    numPlayers = count


def getPlayerCount():
    global numPlayers
    numPlayers = -1
    buttonWidth = 50
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitApp()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    numPlayers = 0
                elif event.key == pygame.K_1:
                    numPlayers = 1
                elif event.key == pygame.K_2:
                    numPlayers = 2

        if numPlayers != -1:
            print('{} human\t{} computer'.format(numPlayers, 2-numPlayers))
            gameLoop()

        window.fill(COLORS.WHITE)
        button('0', (windowWidth//2 - buttonWidth//2 - buttonWidth - windowWidth//10, windowHeight//2 - buttonWidth//2), (buttonWidth, buttonWidth), COLORS.DARK_RED, COLORS.RED, setPlayerCount, 0, textSize=30)
        button('1', (windowWidth//2 - buttonWidth//2, windowHeight//2 - buttonWidth//2), (buttonWidth, buttonWidth), COLORS.DARK_RED, COLORS.RED, setPlayerCount, 1, textSize=30)
        button('2', (windowWidth//2 + buttonWidth//2 + windowWidth//10, windowHeight//2 - buttonWidth//2), (buttonWidth, buttonWidth), COLORS.DARK_RED, COLORS.RED, setPlayerCount, 2, textSize=30)

        pygame.display.update()
        clock.tick(60)


def gameLoop():
    board = np.zeros((6, 7))
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitApp()

        window.fill(COLORS.WHITE)
        pygame.display.update()
        clock.tick(60)


def ConnectFour():
    global windowWidth
    global windowHeight
    global clock
    global window
    windowWidth = 1000
    windowHeight = 800

    pygame.init()
    window = pygame.display.set_mode((windowWidth, windowHeight))
    pygame.display.set_caption('Connect Four')
    clock = pygame.time.Clock()
    getPlayerCount()


if __name__ == '__main__':
    ConnectFour()
