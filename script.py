import pygame
import numpy as np
import os
import sys
import random

#colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)

dim = int(sys.argv[1])
#dim = 28
p = float(sys.argv[2])

#figure out proper scaling
height =20 
width = height
margin = 5

#show maze
def display_Maze(grid):
    for row in range(dim):
            for column in range(dim):
                color = WHITE
                if grid[row][column] == 1:
                    color = BLACK
                pygame.draw.rect(screen, color, [(margin + width) * column + margin,
                                                 (margin+ height) * row + margin,
                                                 width, height])
    clock.tick(60)
    pygame.display.flip()

grid = []
for row in range(dim):
    grid.append([])
    for column in range(dim):
        if(random.uniform(0.,1.) < p):
            grid[row].append(1)
        else:
            grid[row].append(0)
print(grid)

pygame.init()

size = [710, 710]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MaizOnFire")
clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(BLACK)
    for row in range(dim):
            for column in range(dim):
                color = WHITE
                if grid[row][column] == 1:
                    color = BLACK
                pygame.draw.rect(screen, color, [(margin + width) * column + margin,
                                                 (margin+ height) * row + margin,
                                                 width, height])
    clock.tick(60)
    pygame.display.flip()

