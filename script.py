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

################## TO DO
#
#   WHY DOES LINE 132, 194, 259 CHECK IF NODE IN CLOSED??
#   WHEN LINE 140, 202, 267 CHECKS THE SAME FREAKING THING??????
#  
#   WHY DO WE EVEN HAVE A CLOSED SET WHEN WE CAN JUST CHECK THE SQUARE COLOR?
#
###################


def generate_Maze():
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
            clear = grid[row][col] == sa.Status.VISITED or grid[row][col] == sa.Status.FRINGE or grid[row][col] == sa.Status.PATH

            if(clear):
                grid[row][col] = sa.Status.FREE 





dim = int(sys.argv[1])
p = float(sys.argv[2])

#main

grid = generate_Maze()


done = False

if sa.dfs(grid, 0,0,dim-1,dim-1):
    print("Found goal, performing bfs")
    sa.display_Maze(grid)
    time.sleep(1)
    clear_Search(grid)
    sa.bfs(grid, 0,0, dim-1, dim-1)
    print("Found goal, performing A*")
    sa.display_Maze(grid)
    time.sleep(1)
    clear_Search(grid)
    sa.a_star(grid, 0, 0, dim-1, dim-1)
    print("Done!")
    while not done:
        sa.display_Maze(grid)
else:
    print("Failure")
    while not done:
        sa.display_Maze(grid)


