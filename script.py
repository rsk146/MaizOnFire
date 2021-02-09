import pygame
import numpy as np
import os
import sys
import random
from collections import deque
from queue import PriorityQueue
from math import sqrt
import math
from enum import Enum

################## TO DO
#
#   Refactor BFS
#       Make sure to include enums and include backtracing
#   Refactor A_star
#       Make sure to include enums and include backtracing
#
#   Separate the main algos from the display stuff and import it
###################


#colors
WHITE = (255, 255, 255) #Free = 0
BLACK = (0,0,0)         #Walls = 1
BLUE = (0, 0, 255)      #Player = 2
RED = (255, 0, 0)       #Goal = 3
GREEN = (0, 100, 0)     #In Fringe = 4
L_GREEN = (0, 255, 0)   #Visited = 5
YELLOW = (0, 255, 255)  #Fire = 6
PURPLE = (255,0,255)    #Parent = 7

class Status(Enum):
    FREE = 0
    WALL = 1
    PLAYER = 2
    GOAL = 3
    FRINGE = 4
    VISITED = 5
    FIRE = 6
    PATH = 7

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

                color = BLACK
                if grid[row][column] == Status.FREE:
                    color = WHITE
                elif grid[row][column] == Status.PLAYER:
                    color = BLUE
                elif grid[row][column] == Status.GOAL:
                    color = RED
                elif grid[row][column] == Status.FRINGE:
                    color = L_GREEN
                elif grid[row][column] == Status.VISITED:
                    color = GREEN
                elif grid[row][column] == Status.FIRE:
                    color = YELLOW
                elif grid[row][column] == Status.PATH:
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

    parentGrid = []
    for row in range(dim):
        parentGrid.append([])
        for col in range(dim):
            parentGrid[row].append((0,0))

    
    directions = ((0,-1), (-1,0), (1,0),(0,1))
    
    while fringe:
        #Get x,y of next node to search from our stack
        current = fringe.pop()
        curX = current[0]
        curY = current[1]

        #If we've reached the goal node, then trace the path and return
        if(curX == dim-1 and curY == dim-1):
            grid[curX][curY] = Status.PATH
            backtrace(grid, parentGrid)
            return True
        
        #Otherwise, search for next nodes to add to fringe
        for (dirX, dirY) in directions:
            #Get the next node (priority determined by order of "directions")
            nextX = curX + dirX
            nextY = curY + dirY
            nextNode = (nextX, nextY)

            #If the node is already visited, go next
            if(nextNode in closed_set):
                continue
            
            #If next node is in bounds, check it
            if(nextX >=0 and nextX < dim and nextY >= 0 and nextY < dim):
                #If its not a wall and not visited, add to fringe. Mark current node as parent of next
                if(grid[nextX][nextY] != Status.WALL and nextNode not in closed_set):
                    #If next node is already in fringe, then there was a shorter path to that node, don't overwrite
                    if(nextNode not in fringe):
                        parentGrid[nextX][nextY] = current
                    fringe.append(nextNode)
                    grid[nextX][nextY] = Status.FRINGE
            

        #We are done with this node since we've checked all neighbors
        closed_set.add(current)
        grid[curX][curY] = Status.VISITED
        display_Maze(grid)
    
    #If we make it here, we've went through the whole fringe and could not find path to end
    print("Goal not reached")
    return False

    # while fringe:
    #     current = fringe.pop()
    #     x = current[0]
    #     y = current[1]
        
    #     if current == (dim-1, dim-1):
    #         print("Goal Reached")
    #         grid[x][y] = 7
    #         backtrace(grid, parentGrid)
    #         return True
    #     else:
    #         if current not in closed_set:
    #             if parent is not None: 
    #                 grid[parent[0]][parent[1]] = 5

    #             if( x-1 >=0 and grid[x-1][y] != 1 and (x-1, y) not in closed_set):
    #                 fringe.append((x-1, y))
    #                 grid[x-1][y] = 4
    #                 parentGrid[x-1][y] = current

    #             if( y-1 >=0 and grid[x][y-1] != 1 and (x, y-1) not in closed_set):
    #                 fringe.append((x, y-1))
    #                 grid[x][y-1] = 4
    #                 parentGrid[x][y-1] = current

    #             if( x+1 < dim and grid[x+1][y] != 1 and (x+1, y) not in closed_set):
    #                 fringe.append((x+1, y))
    #                 grid[x+1][y] = 4
    #                 parentGrid[x+1][y] = current

    #             if( y+1 < dim and grid[x][y+1] != 1) and (x, y+1) not in closed_set:
    #                 fringe.append((x, y+1))
    #                 grid[x][y+1] = 4
    #                 parentGrid[x][y+1] = current

    #             closed_set.add(current)
    #             grid[x][y] = 2
    #             parent = current
    #     display_Maze(grid)
    
    # print("Goal not reached")

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

def backtrace(maze, parentGrid):
    #Start at the goal node
    curX = dim -1
    curY = dim -1

    #Set the current node to be part of the path
    #Use ParentGrid to find the previously visited node
    #Set current X and Y to the parent of the node we are at
    #Keep looping this until we reach the start
    while(curX != 0 or curY != 0):
        maze[curX][curY] = Status.PATH

        parCoor = parentGrid[curX][curY]
        curX = parCoor[0]
        curY = parCoor[1]

    maze[0][0] = Status.PATH


#main
grid = []
for row in range(dim):
    grid.append([])
    for column in range(dim):
        if(random.uniform(0.,1.) < p):
            grid[row].append(Status.WALL)
        else:
            grid[row].append(Status.FREE)

grid[0][0] = Status.PLAYER
grid[dim-1][dim-1] = Status.GOAL

pygame.init()

size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MaizOnFire")
clock = pygame.time.Clock()
done = False

if dfs(grid):
    print("Found goal")
    while not done:
        display_Maze(grid)
else:
    print("Failure")
    while not done:
        display_Maze(grid)


