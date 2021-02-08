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

        if current == (dim-1, dim-1):
            print("Goal Reached")
            grid[current[0]][current[1]] = 7
            return True
        else:
            if current not in closed_set:
                if parent is not None: 
                    grid[parent[0]][parent[1]] = 5
                if(current[0] -1 >=0 and grid[current[0]-1][current[1]] != 1 and (current[0]-1, current[1]) not in closed_set):
                    fringe.append((current[0]-1, current[1]))
                    grid[current[0]-1][current[1]] = 4
                if(current[1] -1 >=0 and grid[current[0]][current[1]-1] != 1 and (current[0], current[1]-1) not in closed_set):
                    fringe.append((current[0], current[1]-1))
                    grid[current[0]][current[1]-1] = 4
                if(current[0] +1 < dim and grid[current[0]+1][current[1]] != 1 and (current[0]+1, current[1]) not in closed_set):
                    fringe.append((current[0]+1, current[1]))
                    grid[current[0]+1][current[1]] = 4
                if(current[1] +1 < dim and grid[current[0]][current[1]+1] != 1) and (current[0], current[1]+1) not in closed_set:
                    fringe.append((current[0], current[1]+1))
                    grid[current[0]][current[1]+1] = 4
                closed_set.add(current)
                grid[current[0]][current[1]] = 2
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

        if current == (dim-1, dim-1):
            print("Goal Reached")
            grid[current[0]][current[1]] = 7
            return True
        else:
            if current not in closed_set:
                if parent is not None: 
                    grid[parent[0]][parent[1]] = 5
                if(current[0] -1 >=0 and grid[current[0]-1][current[1]] != 1 and (current[0]-1, current[1]) not in closed_set):
                    fringe.append((current[0]-1, current[1]))
                    grid[current[0]-1][current[1]] = 4
                if(current[1] -1 >=0 and grid[current[0]][current[1]-1] != 1 and (current[0], current[1]-1) not in closed_set):
                    fringe.append((current[0], current[1]-1))
                    grid[current[0]][current[1]-1] = 4
                if(current[0] +1 < dim and grid[current[0]+1][current[1]] != 1 and (current[0]+1, current[1]) not in closed_set):
                    fringe.append((current[0]+1, current[1]))
                    grid[current[0]+1][current[1]] = 4
                if(current[1] +1 < dim and grid[current[0]][current[1]+1] != 1) and (current[0], current[1]+1) not in closed_set:
                    fringe.append((current[0], current[1]+1))
                    grid[current[0]][current[1]+1] = 4
                closed_set.add(current)
                grid[current[0]][current[1]] = 2
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
        print(current)
        print(h)
        if current[2] == dim-1 and current[3] == dim-1:
            print("Goal Reached")
            grid[current[2]][current[3]] = 7
            return True
        else:
            if (current[2],current[3]) not in closed_set:
        
                if parent is not None: 
                    grid[parent[2]][parent[3]] = 5

                #Heuristic is calculated wrong. We calculated distance away from start rather than distance to the end
                
                if(current[2] -1 >=0 and grid[current[2]-1][current[3]] != 1 and (current[2]-1, current[3]) not in closed_set):
                    h = sqrt((dim - current[2])**2 + (dim - current[3]-1)**2)
                    fringe.put((current[1] + 1 + h,current[1]+1,current[2]-1, current[3]))
                    grid[current[2]-1][current[3]] = 4

                if(current[3] -1 >=0 and grid[current[2]][current[3]-1] != 1 and (current[2], current[3]-1) not in closed_set):
                    h = sqrt((dim - current[2] - 1)**2 + (dim - current[3])**2)
                    fringe.put((current[1] + 1 + h,current[1]+1,current[2], current[3]-1))
                    grid[current[2]][current[3]-1] = 4

                if(current[2] +1 < dim and grid[current[2]+1][current[3]] != 1 and (current[2]+1, current[3]) not in closed_set):
                    h = sqrt((dim - 2 - current[2])**2 + (dim - current[3]-1)**2)
                    fringe.put((current[1] + 1 + h,current[1]+1,current[2]+1, current[3]))
                    grid[current[2]+1][current[3]] = 4

                if(current[3] +1 < dim and grid[current[2]][current[3]+1] != 1) and (current[2], current[3]+1) not in closed_set:
                    h = sqrt((dim - current[2]-1)**2 + (dim - current[3] - 2)**2)
                    fringe.put((current[1] + 1 + h,current[1]+1,current[2], current[3]+1))
                    grid[current[2]][current[3]+1] = 4

                closed_set.add((current[2], current[3]))
                grid[current[2]][current[3]] = 2
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


