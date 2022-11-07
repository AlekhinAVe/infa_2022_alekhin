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
global X
X = []
global Y
Y = []
global R
R = []
global quantity
quantity = 1


def new_ball():
    global x, y, r
    x = randint(100,700)
    y = randint(100,500)
    r = randint(30,50)
    X.append(x)
    Y.append(y)
    R.append(r)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def click(event, quantity):
    global scores
    p = 0
    for i in range(quantity):
        a = ((event[0] - X[i]) ** 2 + (event[1] - Y[i]) ** 2) ** 0.5
        if a < R[i]:
            p += 1
        else:
            continue
    if p > 0:
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
            if (click(event.pos, quantity)):
                screen.fill(BLACK)
                X=[]
                Y=[]
                R=[]
                quantity = randint(1, 5)
                for i in range(quantity):
                    new_ball()
    pygame.display.update()


pygame.quit()