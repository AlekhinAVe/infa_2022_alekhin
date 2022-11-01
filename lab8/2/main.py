import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 30
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
global scores
scores = 0

def new_ball():
    global x, y, r
    x = randint(100,700)
    y = randint(100,500)
    r = randint(30,50)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def click(event):
    global scores
    X = event[0]
    Y = event[1]
    a = ((X-x)**2+(Y-y)**2)**0.5
    if a < r:
        scores += 1
        print(scores)
        return True
    else:
        return False

pygame.display.update()
clock = pygame.time.Clock()
finished = False

new_ball()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (click(event.pos)):
                screen.fill(BLACK)
                new_ball()
                new_ball()
    pygame.display.update()


pygame.quit()