import pygame
import numpy as np
import os
import sys
import random

#colors
WHITE = (255, 255, 255) #Free = 0
BLACK = (0,0,0)         #Walls = 1
BLUE = (0, 0, 255)      #Player = 2
RED = (255, 0, 0)       #Goal = 3
L_GREEN = (0, 100, 0)   #In Fringe = 4
GREEN = (0, 255, 0)     #Visited = 5
YELLOW = (0, 255, 255)  #Fire = 6

#dim = sys.argv[1]
dim = 28
#p = sys.argv[2]
p = 0.2

#figure out proper scaling
height =20 
width = height
margin = 5

#show maze
def display_Maze(grid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    for row in range(28):
            for column in range(28):
                color = WHITE
                if grid[row][column] == 1:
                    color = BLACK
                elif grid[row][column] == 2:
                    color = BLUE
                elif grid[row][column] == 3:
                    color = RED
                pygame.draw.rect(screen, color, [(margin + width) * column + margin,
                                                 (margin+ height) * row + margin,
                                                 width, height])
    clock.tick(60)
    pygame.display.flip()

grid = []
for row in range(dim):
    grid.append([])
    for column in range(dim):
        if(random.uniform(0,1) < p):
            grid[row].append(1)
        else:
            grid[row].append(0)
grid[0][0] = 2
grid[dim-1][dim-1] = 3

pygame.init()

size = [710, 710]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MaizOnFire")
clock = pygame.time.Clock()
done = False

print("in loop")
while not done:
    display_Maze(grid)

