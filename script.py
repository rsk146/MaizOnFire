import searchAlgos as sa
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
import copy

################## TO DO
#
#   WHY DOES LINE 132, 194, 259 CHECK IF NODE IN CLOSED??
#   WHEN LINE 140, 202, 267 CHECKS THE SAME FREAKING THING??????
#  
#   WHY DO WE EVEN HAVE A CLOSED SET WHEN WE CAN JUST CHECK THE SQUARE COLOR?
#
#   -Add check to see if there is a path from fire to player
#   -Maybe add another color to show path that player has taken already
#  
#
#
###################


def generate_Maze(dim, p):
    grid = []
    for row in range(dim):
        grid.append([])
        for column in range(dim):
            if(random.uniform(0.,1.) < p):
                grid[row].append(sa.Status.WALL)
            else:
                grid[row].append(sa.Status.FREE)

    grid[0][0] = sa.Status.PLAYER
    grid[dim-1][dim-1] = sa.Status.GOAL
    return grid

def clear_Search(grid):
    for row in range(dim):
        for col in range(dim):
            clear = grid[row][col] == sa.Status.VISITED or grid[row][col] == sa.Status.FRINGE

            if(clear):
                grid[row][col] = sa.Status.FREE 
def clear_Path(grid):
    for row in range(dim):
        for col in range(dim):
            if(grid[row][col] == sa.Status.PATH):
                grid[row][col] = sa.Status.FREE

def add_valid_fire(grid):
    valid = False
    
    while not valid:
        fireX = int(random.uniform(0, dim-1))
        fireY = int(random.uniform(0, dim-1))

        #make sure fire not on player or exit
        if((fireX != 0 or fireY != 0) and (fireX != dim-1 or fireY !=dim-1)):
            valid = True

        #Eventually Add check to see if there is path from fire to player!!

    grid[fireX][fireY] = sa.Status.FIRE
    return (fireX, fireY)

def spread_fire(grid):
    oldGrid = copy.deepcopy(grid)
    for row in range(dim):
        for col in range(dim):
            if(oldGrid[row][col] == sa.Status.FIRE or oldGrid[row][col] == sa.Status.WALL):
                continue

            adjFire = count_fire(oldGrid, row, col)
            pFire = 1 - (1-q)**adjFire
            if(random.uniform(0.,1.) < pFire):
                grid[row][col] = sa.Status.FIRE

def count_fire(oldGrid, row, col):
    count = 0
    for i in range(2):
        for j in range(-1,2,2):
            if i == 0:
                rowCheck = row
                colCheck = col + j
            else:
                colCheck = col
                rowCheck = row + j
            if(rowCheck >=0 and rowCheck < dim and colCheck >= 0 and colCheck < dim):
                if(oldGrid[rowCheck][colCheck] == sa.Status.FIRE):
                    count = count + 1
    return count

def performStrategyOne(grid):
    playerX = 0
    playerY = 0
    
    if(not sa.a_star(grid, 0, 0, dim-1, dim -1)):
        print("Not possible to escape the maiz")
        return False
    
    clear_Search(grid)
    sa.display_Maze(grid)
    time.sleep(0.5)

    while (playerX,playerY) != (dim-1, dim-1):
        (playerX, playerY) = path_step(grid, playerX, playerY)
        spread_fire(grid)
        sa.display_Maze(grid)
        if(grid[playerX][playerY] == sa.Status.FIRE):
            print("Player died to fire")
            return False
        
        time.sleep(0.3)
    
    print("Player escaped the MaizOfFire")
    return True

def performStrategyTwo(grid):
    playerX = 0
    playerY = 0
    endDim = dim-1
    if(not sa.a_star(grid, 0, 0, endDim, endDim)):
        print("Not possible to escape the maiz")
        return False
    
    clear_Search(grid)

    while (playerX,playerY) != (endDim, endDim):
        sa.display_Maze(grid)
        time.sleep(0.3)
        clear_Search(grid)
        (playerX, playerY) = path_step(grid, playerX, playerY)
        clear_Path(grid)
        spread_fire(grid)
        if(grid[playerX][playerY] == sa.Status.FIRE):
            print("Player died to fire")
            return False
        
        if(not sa.a_star(grid, playerX, playerY, endDim, endDim)):
            print("It is no longer possible to escape the maiz")
            return False
        
    
    print("Player escaped the MaizOfFire")
    return True

def path_step(grid, row, col):
    #Copy pasted from Fire checker cuz im lazy to check 4 nodes
    for i in range(2):
        for j in range(-1,2,2):
            if i == 0:
                rowCheck = row
                colCheck = col + j
            else:
                colCheck = col
                rowCheck = row + j
            if(rowCheck >=0 and rowCheck < dim and colCheck >= 0 and colCheck < dim):
                if(grid[rowCheck][colCheck] == sa.Status.PATH or grid[rowCheck][colCheck] == sa.Status.GOAL):
                    grid[row][col] = sa.Status.FREE
                    grid[rowCheck][colCheck] = sa.Status.PLAYER
                    return (rowCheck,colCheck)

    #print("yoo")
    return (row,col)


def collect_dfs_data(trials):
    count = 0
    print("Showing DFS Data Values with dim = " + str(dim) + ", trials = " + str(trials))
    for prob in range(1, 10):
        p = float(prob/10)
        count = 0
        for x in range(trials):
            grid = generate_Maze(dim, p)
            if(sa.dfs(grid, 0, 0, dim-1, dim-1)):
                count+=1
        print("P= " + str(p) + ", count = " + str(count))

    return

def collect_bfs_astar_data(trials):
    print("Showing BFS and A* Data Values with dim = " + str(dim) + ", trials = " + str(trials))
    for prob in range(1,20):
        p = float(prob)/20
        diff_total = 0
        for x in range(trials):
            grid = generate_Maze(dim,p)
            bfs_num_nodes_checked = sa.bfs(grid, 0,0, dim-1, dim-1)
            astar_num_nodes_checked = sa.a_star(grid, 0,0, dim-1, dim-1)
            if bfs_num_nodes_checked - astar_num_nodes_checked < 0:
                print("CALL THE AMBULANCE")
            diff_total += bfs_num_nodes_checked - astar_num_nodes_checked
        print("P = " + str(p) + ", avg difference = " + str(diff_total/trials))


'''def performStrategyThree(grid, fire_start):
    copyGrid = copy.deepcopy(grid)
    if a_star(copyGrid, fire_start[0], fire_start[1], ):'''

dim = int(sys.argv[1])
p2 = float(sys.argv[2])

fireActive = len(sys.argv) == 4

if(fireActive):
    q = float(sys.argv[3])
else:
    q = 0


#grid = generate_Maze(dim, p)
# if(fireActive):
#     add_valid_fire(grid)

#collect_dfs_data(10000)
collect_bfs_astar_data(10)


'''
performStrategyTwo(grid)
while not done:
    sa.display_Maze(grid)

#For Raky if you want to see all of the algos

if sa.dfs(grid, 0,0,dim-1,dim-1):
    print("Found goal, performing bfs")
    sa.display_Maze(grid)
    time.sleep(1)
    clear_Search(grid)
    clear_Path(grid)
    sa.bfs(grid, 0,0, dim-1, dim-1)
    print("Found goal, performing A*")
    sa.display_Maze(grid)
    time.sleep(1)
    clear_Search(grid)
    clear_Path(grid)
    sa.a_star(grid, 0, 0, dim-1, dim-1)
    print("Done!")
    while not done:
        sa.display_Maze(grid)
else:
    print("Failure")
    while not done:
        sa.display_Maze(grid)
'''
