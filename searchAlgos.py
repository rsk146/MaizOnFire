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
import time

class Status(Enum):
    PATH = 0
    GOAL = 1
    PLAYER = 2
    FREE = 3
    VISITED = 4
    FRINGE = 5
    WALL = 6
    FIRE = 7

#colors
WHITE = (255, 255, 255) #Free 
BLACK = (0,0,0)         #Walls 
BLUE = (0, 0, 255)      #Player 
RED = (255, 0, 0)       #Goal 
GREEN = (0, 100, 0)     #In Fringe 
L_GREEN = (0, 255, 0)   #Visited 
YELLOW = (255, 255, 0)  #Fire 
PURPLE = (255,0,255)    #Parent 

pygame.init()
size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MaizOnFire")
clock = pygame.time.Clock()
dim = int(sys.argv[1])
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
    clock.tick(300)
    pygame.display.flip()

#show path
def backtrace(maze, parentGrid, startX, startY, endX, endY):
    #Start at the goal node
    curX = endX
    curY = endY
    count = 0
    #Set the current node to be part of the path
    #Use ParentGrid to find the previously visited node
    #Set current X and Y to the parent of the node we are at
    #Keep looping this until we reach the start
    while(curX != startX or curY != startY):
        maze[curX][curY] = Status.PATH
        parCoor = parentGrid[curX][curY]
        curX = parCoor[0]
        curY = parCoor[1]
        count = count + 1

    return count


def dfs(grid, startX, startY, endX, endY):
    startStatus = grid[startX][startY]
    endStatus = grid[endX][endY]
    fringe = [(startX, startY)]
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
        if(curX == endX and curY == endY):
            print(backtrace(grid, parentGrid, startX, startY, endX, endY))
            grid[startX][startY] = startStatus
            grid[endX][endY] = endStatus
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
                #If square is free (not wall, visited, in fringe, or on fire), add to fringe. Mark current node as parent of next
                availibleSquare = bool(grid[nextX][nextY] == Status.FREE or grid[nextX][nextY] == Status.GOAL)

                if(availibleSquare and nextNode not in closed_set):
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

def bfs(grid, startX, startY, endX, endY):
    startStatus = grid[startX][startY]
    endStatus = grid[endX][endY]
    fringe = deque()
    fringe.append((startX, startY))
    closed_set = set()
    counter = 0
    
    parentGrid = []
    for row in range(dim):
        parentGrid.append([])
        for col in range(dim):
            parentGrid[row].append((0,0))

    directions = ((0,-1), (-1,0), (1,0),(0,1))
    
    while fringe:
        #Get x,y of next node to search from our stack
        current = fringe.popleft()
        counter +=1
        curX = current[0]
        curY = current[1]

        #If we've reached the goal node, then trace the path and return
        if(curX == endX and curY == endY):
            print(backtrace(grid, parentGrid, startX, startY, endX, endY))
            grid[startX][startY] = startStatus
            grid[endX][endY] = endStatus
            return counter
        
        #Otherwise, search for next nodes to add to fringe
        for (dirX, dirY) in directions:
            #Get the next node (priority determined by order of "directions")
            nextX = curX + dirX
            nextY = curY + dirY
            nextNode = (nextX, nextY)
            
            #If next node is in bounds, check it
            if(nextX >=0 and nextX < dim and nextY >= 0 and nextY < dim):
                #If the node is already visited, go next
                if(nextNode in closed_set):
                    continue
                
                #If next node is in bounds, check it
                if(nextX >=0 and nextX < dim and nextY >= 0 and nextY < dim):
                #If square is free (not wall, visited, in fringe, or on fire), add to fringe. Mark current node as parent of next
                    availibleSquare = bool(grid[nextX][nextY] == Status.FREE or grid[nextX][nextY] == Status.GOAL)
                
                    if(availibleSquare and nextNode not in closed_set):
                        parentGrid[nextX][nextY] = current
                        fringe.append(nextNode)
                        grid[nextX][nextY] = Status.FRINGE
            

        #We are done with this node since we've checked all neighbors
        closed_set.add(current)
        grid[curX][curY] = Status.VISITED
        display_Maze(grid)
    
    return False

#Uses Euclidean distance as heuristic
def a_star(grid, startX, startY, endX, endY):
    startStatus = grid[startX][startY]
    endStatus = grid[endX][endY]

    fringe = PriorityQueue()
    beginning = sqrt((abs(endY-startY)-1)**2 + (abs(endX-startX)-1)**2)

    parentGrid = []
    for row in range(dim):
        parentGrid.append([])
        for col in range(dim):
            parentGrid[row].append((startX, startY))

    #(current cost+heuristic, current cost, x, y)
    fringe.put((beginning, 0, startX, startY))
    closed_set = set()

    directions = ((0,-1), (-1,0), (1,0),(0,1))

    while not fringe.empty():

        current = fringe.get()
        #estimatedEndCost = current[0]
        curCost = current[1]
        curX = current[2]
        curY = current[3]


        if(curX == endX and curY == endY):
            print(backtrace(grid, parentGrid, startX, startY, endX, endY))
            grid[startX][startY] = startStatus
            grid[endX][endY] = endStatus
            return True
    
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
                
                #If square is free (not wall, visited, in fringe, or on fire), add to fringe. Mark current node as parent of next
                availibleSquare = bool(grid[nextX][nextY] == Status.FREE or grid[nextX][nextY] == Status.GOAL)
                if(availibleSquare and nextNode not in closed_set):
                    
                    h = sqrt((abs(endY-nextY)-1)**2 + (abs(endX-nextX)-1)**2)
                    nextNodeCost = curCost + 1
                    estEndCost = nextNodeCost + h

                    parentGrid[nextX][nextY] = (curX, curY)
                    fringe.put((estEndCost, nextNodeCost, nextX, nextY))
                    grid[nextX][nextY] = Status.FRINGE
            

        #We are done with this node since we've checked all neighbors
        closed_set.add((curX, curY))
        if(curX != startX or curY != startY):
            grid[curX][curY] = Status.VISITED
        display_Maze(grid)
    
    print("Goal not reached")
    return False



def uselessfunction():
    return

