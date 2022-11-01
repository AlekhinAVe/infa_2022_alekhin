import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((255, 255, 255))

circle(screen, (255, 255, 0), (200, 175), 100)
circle(screen, (0, 0, 0), (200, 175), 100, 5)

circle(screen, (255, 0, 0), (235, 150), 20)
circle(screen, (0, 0, 0), (235, 150), 20, 5)
circle(screen, (0, 0, 0), (235, 150), 10)

circle(screen, (255, 0, 0), (165, 150), 20)
circle(screen, (0, 0, 0), (165, 150), 20, 5)
circle(screen, (0, 0, 0), (165, 150), 10)

rect(screen, (0, 0, 0), (150, 205, 100, 15))

polygon(screen, (0, 0, 0), [(175,135), (180,130),
                               (115,80), (110,85)])

polygon(screen, (0, 0, 0), [(225,135), (220,130),
                               (285,80), (290,85)])

pygame.display.update()
clock = pygame.time.Clock()
finished = False

screen.fill((255, 255, 0))

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()