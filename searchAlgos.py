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

#K
#enumeration used to represent the different objects in a square of the maze
class Status(Enum):
    PATH = 0
    GOAL = 1
    PLAYER = 2
    FREE = 3
    VISITED = 4
    FRINGE = 5
    WALL = 6
    FIRE = 7

#colors for our visualization to see the maze and traversals
WHITE = (255, 255, 255) #Free 
BLACK = (0,0,0)         #Walls 
BLUE = (0, 0, 255)      #Player 
RED = (255, 0, 0)       #Goal 
GREEN = (0, 100, 0)     #In Fringe 
L_GREEN = (0, 255, 0)   #Visited 
YELLOW = (255, 255, 0)  #Fire 
PURPLE = (255,0,255)    #Parent 

#R
#initializations for the screen size, square size, etc. for the visualization
pygame.init()
size = [800, 800]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MaizOnFire")
clock = pygame.time.Clock()
dim = int(sys.argv[1])
height = 800/dim-4  
width = height
margin = 4

#R
#calls to the pygame library to show the maze for it's different values in it's entries
def display_Maze(grid):
    #check if exiting the visualization, then exit the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
    #loop over all maze entries and set the color appropriately based on the enum value in the maze
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
                #draw this square on the visualization with the appropriate color
                pygame.draw.rect(screen, color, [(margin + width) * column + margin,
                                                (margin+ height) * row + margin,
                                                width, height])
    #fps for updating the maze visually
    clock.tick(60)
    #update display
    pygame.display.flip()
    return

#K
#adds the squares that would be on the path taken upon reaching the end by backtracing through the squares and the parent grid
#returns the length of the path
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

#R
#run depth first search on a maze, not allowed to land on squares that are not free
def dfs(grid, startX, startY, endX, endY):
    startStatus = grid[startX][startY]
    endStatus = grid[endX][endY]
    #fringe is a LIFO stack, using the python list and pop()
    fringe = [(startX, startY)]
    #closed set to check if visited already
    closed_set = set()
    #parent grid to see where we got to each square from
    parentGrid = []
    for row in range(dim):
        parentGrid.append([])
        for col in range(dim):
            parentGrid[row].append((0,0))

    #deltas for where we can go from a square. down, left, right, up
    directions = ((0,-1), (-1,0), (1,0),(0,1))
    
    while fringe:
        #Get x,y of next node to search from our stack
        current = fringe.pop()
        curX = current[0]
        curY = current[1]

        #If we've reached the goal node, then trace the path and return
        if(curX == endX and curY == endY):
            pathLen = backtrace(grid, parentGrid, startX, startY, endX, endY)
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
    #print("Goal not reached")
    return False

#R
#run breadth first search on the maze, not allowed to land on squares that are not free
def bfs(grid, startX, startY, endX, endY):
    startStatus = grid[startX][startY]
    endStatus = grid[endX][endY]
    #fringe is a FIFO queue from queue library
    fringe = deque()
    fringe.append((startX, startY))
    #closed set to check if visited already
    closed_set = set()
    #counter for checking number of visited nodes
    counter = 0
    #parent grid to see where we got to each square from 
    parentGrid = []
    for row in range(dim):
        parentGrid.append([])
        for col in range(dim):
            parentGrid[row].append((0,0))
    #deltas for where we can go from a square. down, left, right, up
    directions = ((0,-1), (-1,0), (1,0),(0,1))
    
    while fringe:
        #Get x,y of next node to search from our queue
        current = fringe.popleft()
        counter +=1
        curX = current[0]
        curY = current[1]

        #If we've reached the goal node, then trace the path and return
        if(curX == endX and curY == endY):
            pathLen = backtrace(grid, parentGrid, startX, startY, endX, endY)
            grid[startX][startY] = startStatus
            grid[endX][endY] = endStatus
            #returns nodes visited
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
    
    #returns the number of nodes visited for failure as well. 
    #Sometimes changed to return 0 if we care about success/failure instead of nodes visited
    return counter
    #return 0

#K
#run a* using Euclidean distance as heuristic
def a_star(grid, startX, startY, endX, endY):
    #counter for number of nodes visited
    count = 0
    startStatus = grid[startX][startY]
    endStatus = grid[endX][endY]
    #fringe is a heap from queue library
    fringe = PriorityQueue()
    beginning = sqrt((abs(endY-startY)-1)**2 + (abs(endX-startX)-1)**2)
    #parent grid to see where we got to each square from
    parentGrid = []
    for row in range(dim):
        parentGrid.append([])
        for col in range(dim):
            parentGrid[row].append((startX, startY))

    #(current cost+heuristic, current cost, x, y)
    fringe.put((beginning, 0, startX, startY))
    closed_set = set()

    #deltas for where we can go from a square. down, left, right, up
    directions = ((0,-1), (-1,0), (1,0),(0,1))

    while not fringe.empty():

        current = fringe.get()
        count+=1
        curCost = current[1]
        curX = current[2]
        curY = current[3]


        if(curX == endX and curY == endY):
            pathLen = backtrace(grid, parentGrid, startX, startY, endX, endY)
            grid[startX][startY] = startStatus
            grid[endX][endY] = endStatus
            return count
    
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
    
    #print("Goal not reached")
    #returns the number of nodes explored even for failure
    #sometimes returns 0 if we care about success/failure instead of nodes visited 
    return count
    #return 0


#???????????? what thr fuck
def uselessfunction():
    return

