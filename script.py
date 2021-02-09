import pygame
import numpy as np
import os
import sys
import random
from collections import deque
from queue import PriorityQueue
from math import sqrt
import math

#colors
WHITE = (255, 255, 255) #Free = 0
BLACK = (0,0,0)         #Walls = 1
BLUE = (0, 0, 255)      #Player = 2
RED = (255, 0, 0)       #Goal = 3
GREEN = (0, 100, 0)   #In Fringe = 4
L_GREEN = (0, 255, 0)     #Visited = 5
YELLOW = (0, 255, 255)  #Fire = 6
PURPLE = (255,0,255)    #Parent = 7

dim = int(sys.argv[1])
#dim = 28
p = float(sys.argv[2])

#figure out proper scaling
height = 800/dim-4  
width = height
margin = 4

#show maze
def display_Maze(grid):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    for row in range(dim):
            for column in range(dim):
                color = WHITE
                if grid[row][column] == 1:
                    color = BLACK
                elif grid[row][column] == 2:
                    color = BLUE
                elif grid[row][column] == 3:
                    color = RED
                elif grid[row][column] == 4:
                    color = L_GREEN
                elif grid[row][column] == 5:
                    color = GREEN
                elif grid[row][column] == 7:
                    color = PURPLE
                pygame.draw.rect(screen, color, [(margin + width) * column + margin,
                                                 (margin+ height) * row + margin,
                                                 width, height])
    clock.tick(60)
    pygame.display.flip()

#dfs
def dfs(grid):
    fringe = [(0,0)]
    closed_set = set()
    parent = None
    while fringe:
        current = fringe.pop()
        x = current[0]
        y = current[1]
        
        if current == (dim-1, dim-1):
            print("Goal Reached")
            grid[x][y] = 7
            return True
        else:
            if current not in closed_set:
                if parent is not None: 
                    grid[parent[0]][parent[1]] = 5

                if( x-1 >=0 and grid[x-1][y] != 1 and (x-1, y) not in closed_set):
                    fringe.append((x-1, y))
                    grid[x-1][y] = 4

                if( y-1 >=0 and grid[x][y-1] != 1 and (x, y-1) not in closed_set):
                    fringe.append((x, y-1))
                    grid[x][y-1] = 4

                if( x+1 < dim and grid[x+1][y] != 1 and (x+1, y) not in closed_set):
                    fringe.append((x+1, y))
                    grid[x+1][y] = 4

                if( y+1 < dim and grid[x][y+1] != 1) and (x, y+1) not in closed_set:
                    fringe.append((x, y+1))
                    grid[x][y+1] = 4

                closed_set.add(current)
                grid[x][y] = 2
                parent = current
        display_Maze(grid)
    
    print("Goal not reached")
    return False

def bfs(grid):
    fringe = deque()
    fringe.append((0,0))
    closed_set = set()
    parent = None
    while fringe:
        current = fringe.popleft()
        
        x = current[0]
        y = current[1]

        if current == (dim-1, dim-1):
            print("Goal Reached")
            grid[x][y] = 7
            return True
        else:
            if current not in closed_set:
                if parent is not None: 
                    grid[parent[0]][parent[1]] = 5
                if(x -1 >=0 and grid[x-1][y] != 1 and (x-1, y) not in closed_set):
                    fringe.append((x-1, y))
                    grid[x-1][y] = 4
                if(y -1 >=0 and grid[x][y-1] != 1 and (x, y-1) not in closed_set):
                    fringe.append((x, y-1))
                    grid[x][y-1] = 4
                if(x +1 < dim and grid[x+1][y] != 1 and (x+1, y) not in closed_set):
                    fringe.append((x+1, y))
                    grid[x+1][y] = 4
                if(y +1 < dim and grid[x][y+1] != 1) and (x, y+1) not in closed_set:
                    fringe.append((x, y+1))
                    grid[x][y+1] = 4
                closed_set.add(current)
                grid[x][y] = 2
                parent = current
        display_Maze(grid)
    
    print("Goal not reached")
    return False


#Uses Euclidean distance as heuristic
def a_star(grid):
    fringe = PriorityQueue()
    beginning = (dim-1) * sqrt(2)
    #(current cost+heuristic, current cost, x, y)
    fringe.put((beginning, 0, 0, 0))
    closed_set = set()
    parent = None
    h = 0
    while not fringe.empty():

        current = fringe.get()
        estimatedEndCost = current[0]
        currentCost = current[1]
        x = current[2]
        y = current[3]

        print(current)
        print(h)
        if x == dim-1 and y == dim-1:
            print("Goal Reached")
            grid[x][y] = 7
            return True
        else:
            if (x,y) not in closed_set:
        
                if parent is not None: 
                    grid[parent[2]][parent[3]] = 5

                
                if(x -1 >=0 and grid[x-1][y] != 1 and (x-1, y) not in closed_set):
                    h = sqrt((dim - x)**2 + (dim - y-1)**2)
                    fringe.put((currentCost + 1 + h, currentCost+1, x-1, y))
                    grid[x-1][y] = 4

                if(y -1 >=0 and grid[x][y-1] != 1 and (x, y-1) not in closed_set):
                    h = sqrt((dim - x - 1)**2 + (dim - y)**2)
                    fringe.put((currentCost + 1 + h, currentCost+1, x, y-1))
                    grid[x][y-1] = 4

                if(x +1 < dim and grid[x+1][y] != 1 and (x+1, y) not in closed_set):
                    h = sqrt((dim - 2 - x)**2 + (dim - y-1)**2)
                    fringe.put((currentCost + 1 + h, currentCost+1, x+1, y))
                    grid[x+1][y] = 4

                if(y +1 < dim and grid[x][y+1] != 1) and (x, y+1) not in closed_set:
                    h = sqrt((dim - x-1)**2 + (dim - y - 2)**2)
                    fringe.put((currentCost + 1 + h, currentCost+1, x, y+1))
                    grid[x][y+1] = 4

                closed_set.add((x, y))
                grid[x][y] = 2
                parent = current
        display_Maze(grid)
    
    print("Goal not reached")
    return False

#main
grid = []
for row in range(dim):
    grid.append([])
    for column in range(dim):
        if(random.uniform(0.,1.) < p):
            grid[row].append(1)
        else:
            grid[row].append(0)
grid[0][0] = 2
grid[dim-1][dim-1] = 3

pygame.init()

size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MaizOnFire")
clock = pygame.time.Clock()
done = False

if a_star(grid):
    print("Found goal")
    while not done:
        display_Maze(grid)
else:
    print("Failure")
    while not done:
        display_Maze(grid)


