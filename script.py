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
import matplotlib.pyplot as plt

##############Contributions: 
# R above function indicates rsk146 majority contribution
# K above function indicates kjp189 majority contribution
# R/K or K/R indicates both wrote or edited it together and no individual can take majority credit

################## TO DO
#   Report
###################

#R
#Generates a 2d array representation of a maze of dimension dim x dim 
#each square has probability p to be a wall  
def generate_Maze(dim, p):
    #the final maze to be filled and outputted
    grid = []
    #nested for loops to generate all elements up to size dim
    for row in range(dim):
        grid.append([])
        for column in range(dim):
            #checks if a random number is less than p, which is true with probability p and false with probability 1-p
            if(random.uniform(0.,1.) < p):
                #sets value to a wall
                grid[row].append(sa.Status.WALL)
            else:
                #sets value as a free square
                grid[row].append(sa.Status.FREE)
    #sets our start position at beginning
    grid[0][0] = sa.Status.PLAYER
    #sets our goal position at the bottom right
    grid[dim-1][dim-1] = sa.Status.GOAL
    return grid

#K
#clears a maze of any squares that are visited or in the fringe by setting them to free
#operates as a clean up function so we can rerun search algos on a maze after we run them once
def clear_Search(grid):
    for row in range(dim):
        for col in range(dim):
            #boolean to determine if current position in maze is visited or in the fringe
            clear = grid[row][col] == sa.Status.VISITED or grid[row][col] == sa.Status.FRINGE
            #set back to free
            if(clear):
                grid[row][col] = sa.Status.FREE 

#K
#clears the maze of any squares that are the path generated from a search algorithm
#operates as a clean up function so we can rerun search algos on a maze after we run them once              
def clear_Path(grid):
    for row in range(dim):
        for col in range(dim):
            #if the maze value is considered a path, set it to be free
            if(grid[row][col] == sa.Status.PATH):
                grid[row][col] = sa.Status.FREE

#K/R
#generates and returns a maze with a valid, random starting fire square added
#valid means that the agent can reach the goal and the fire can reach the agent so he is in danger
#takes in a dimension n and maze density p to generate the maze
def add_valid_fire(n, p):
    #boolean used for if fire added is valid
    valid = False
    #generates a maze initially with wall density p and dimension n
    grid = generate_Maze(n, p)
    #while we do not have a valid fire entry, keep trying
    while not valid:
        #randomly generated coordinates for the fire's start position
        fireX = int(random.uniform(0, dim-1))
        fireY = int(random.uniform(0, dim-1))
        #make sure fire is not on player start or goal
        if((fireX != 0 or fireY != 0) and (fireX != dim-1 or fireY !=dim-1)):
            #set those fire coordinates to a fire spot
            grid[fireX][fireY] = sa.Status.FIRE
            #checks using dfs if it is possible to reach the end with this maze and fire square
            #using dfs since it is fastest to find if a solution is possible
            fireGoalPath = sa.dfs(grid, 0, 0, n-1, n-1)
            #clear the grid of non wall/fire squares so we can run another search
            clear_Path(grid)
            clear_Search(grid)
            #find if there is a path from the start to the fire to see if there is a way the fire can reach the agent
            grid[fireX][fireY] = sa.Status.GOAL
            #again, using dfs since it is fastest to find if a solution is possible
            firePath = sa.dfs(grid, 0, 0, fireX, fireY)
            #if both paths can be found, the fire is valid. Otherwise, we regenerate the maze and try again
            if not (fireGoalPath and firePath):
                grid = generate_Maze(n,p)
                continue
            valid = True
    #clears the grid from the last dfs
    clear_Search(grid)
    clear_Path(grid)
    #sets the goal and the valid fire node
    grid[fireX][fireY] = sa.Status.FIRE
    grid[n-1][n-1] = sa.Status.GOAL
    #returns the valid maze with valid fire square
    return grid, min(fireGoalPath, firePath)

#K
#spreads the fire to neighboring squares using the flammability q
def spread_fire(grid, q):
    #make a copy of the maze at this point so that we only look at fire squares that can spread this turn, not new ones that were already spread
    oldGrid = copy.deepcopy(grid)
    for row in range(dim):
        for col in range(dim):
            if(oldGrid[row][col] == sa.Status.FIRE or oldGrid[row][col] == sa.Status.WALL):
                continue
            adjFire = count_fire(oldGrid, row, col)
            #find the probability that this square is now on fire, based on the number of adjacent squares that are on fire
            pFire = 1 - (1-q)**adjFire
            #set the value of this square to be on fire pFire% of the time
            if(random.uniform(0.,1.) < pFire):
                grid[row][col] = sa.Status.FIRE

#K
#counts the number of adjacent squares that are on fire and returns that number
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
            #check if the indices in question are valid for the maze
            if(rowCheck >=0 and rowCheck < dim and colCheck >= 0 and colCheck < dim):
                if(oldGrid[rowCheck][colCheck] == sa.Status.FIRE):
                    count = count + 1
    return count

#K
#performs strategy one, outlined in the report on a maze with a valid fire square, with flammability q
#returns true if success, false if failure
def performStrategyOne(grid, q):
    playerX = 0
    playerY = 0
    
    #find the path from the start to the goal before spreading any fire
    if(not sa.a_star(grid, 0, 0, dim-1, dim -1)):
        #print("Not possible to escape the maiz")
        return False
    
    clear_Search(grid)
    sa.display_Maze(grid)
    #time.sleep(0.5)
    
    while (playerX,playerY) != (dim-1, dim-1):
        #walk along the initial path, spreading the fire at each step
        (playerX, playerY) = path_step(grid, playerX, playerY)
        spread_fire(grid, q)
        sa.display_Maze(grid)
        #check if agent runs into a fire square
        if(grid[playerX][playerY] == sa.Status.FIRE):
            #print("Player died to fire")
            return False
        
        #time.sleep(0.3)
    
    #print("Player escaped the MaizOfFire")
    return True

#K
#performs strategy two as outlined in the report
def performStrategyTwo(grid, q):
    playerX = 0
    playerY = 0
    endDim = dim-1

    if(not sa.a_star(grid, 0, 0, endDim, endDim)):
        #print("Not possible to escape the maiz")
        return False
    
    clear_Search(grid)

    while (playerX,playerY) != (endDim, endDim):
        sa.display_Maze(grid)
        #time.sleep(0.3)
        clear_Search(grid)
        #take 1 step along the path found
        (playerX, playerY) = path_step(grid, playerX, playerY)
        clear_Path(grid)
        spread_fire(grid,q)
        if(grid[playerX][playerY] == sa.Status.FIRE):
            #print("Player died to fire")
            return False
        #recalculate the path after spreading the fire once
        if(not sa.a_star(grid, playerX, playerY, endDim, endDim)):
            #print("It is no longer possible to escape the maiz")
            return False
    
    #print("Player escaped the MaizOfFire")
    return True

#K
#takes the player one step forward along the path squares on the grid. 
def path_step(grid, row, col):
    for i in range(2):
        for j in range(-1,2,2):
            if i == 0:
                rowCheck = row
                colCheck = col + j
            else:
                colCheck = col
                rowCheck = row + j
            #checks if indices are valid for the maze
            if(rowCheck >=0 and rowCheck < dim and colCheck >= 0 and colCheck < dim):
                if(grid[rowCheck][colCheck] == sa.Status.PATH or grid[rowCheck][colCheck] == sa.Status.GOAL):
                    grid[row][col] = sa.Status.FREE
                    grid[rowCheck][colCheck] = sa.Status.PLAYER
                    return (rowCheck,colCheck)
    #returns initial position if there is no path squares adjacent
    return (row,col)

#K
#collects success rate data for DFS for a given number of trials for a variety of wall densities
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

#R
#collects number of nodes explored difference data between bfs and a* for a particular maze for a given number of trials and a variety of wall densities
def collect_bfs_astar_data(trials):
    print("Showing BFS and A* Data Values with dim = " + str(dim) + ", trials = " + str(trials))
    for prob in range(1,20):
        p = float(prob)/20
        diff_total = 0
        for x in range(trials):
            grid = generate_Maze(dim,p)
            bfs_num_nodes_checked = sa.bfs(grid, 0,0, dim-1, dim-1)
            clear_Path(grid)
            clear_Search(grid)
            astar_num_nodes_checked = sa.a_star(grid, 0,0, dim-1, dim-1)
            diff_total += bfs_num_nodes_checked - astar_num_nodes_checked
        print("P = " + str(p) + ", avg difference = " + str(diff_total/trials))

#R
#copies the path squares from one maze array into another
def copyPath(finalGrid, pathGrid):
    for row in range(dim):
        for col in range(dim):
            if pathGrid[row][col] == sa.Status.PATH:
                finalGrid[row][col] = sa.Status.PATH

#R
#performs strategy three as detailed in the report
def performStrategyThree(grid, q, dist):
    playerX = 0
    playerY = 0
    #number of steps forward into the future we look
    times = 3
    while (playerX, playerY) != (dim-1, dim-1):
        clear_Path(grid)
        clear_Search(grid)
        while times > 0:
            #copy the maze and spread the fire the appropriate number of times
            copyGrid = copy.deepcopy(grid)
            for i in range(times):
                #spreads fire with 100% flammability in the copy of the maze
                spread_fire(copyGrid, 1)
            sa.display_Maze(copyGrid)
            #checks if path is still possible, otherwise we drop the steps into the future we look and try again
            if not sa.a_star(copyGrid, playerX, playerY, dim-1, dim-1):
                times -=1
                if times == 0:
                    break
            else:
                break
        sa.display_Maze(grid)
        #if we can't go forward looking into the future with 100% flammability, see if we have a possible path at all
        #if we dont, we fail. if we do, take a step along that path and try the algorithm again. 
        if times is 0:
            if not sa.a_star(grid, playerX, playerY, dim-1, dim-1):
                #print("Failed to find a path out")
                return False
            (playerX, playerY) = path_step(grid, playerX, playerY)
            spread_fire(grid, q)
            sa.display_Maze(grid)
            if(grid[playerX][playerY] == sa.Status.FIRE):
                #print("Player died to fire")
                return False
            #time.sleep(.5)
            continue
        #copy the path we found and walk along it the number of steps into the future we looked, while spreading the fire with the given flammability
        copyPath(grid, copyGrid)
        for i in range(times):
            (playerX, playerY) = path_step(grid, playerX, playerY)
            spread_fire(grid, q)
            sa.display_Maze(grid)
            if(grid[playerX][playerY] == sa.Status.FIRE):
                #print("Player died to fire")
                return False
        clear_Search(grid)
        clear_Path(grid)
    #print("Player has exited maze")
    #time.sleep(.5)
    return True

#R
#collects the success rate data per strategy. Each strategy returns a boolean so we count the number of trues for a variety of flammabilities and a wall density of .3
def collect_strategy_data(trials, strategy):
    if strategy == 1:
        print("Showing Strategy One Data with dim = " + str(dim) + ", trials per flammability = " + str(trials))
        for prob in range(1,21):
            q = float(prob)/20
            successes = 0
            for x in range(trials):
                grid = generate_Maze(dim, .3)
                while not sa.a_star(grid, 0, 0, dim-1, dim-1):
                    grid = generate_Maze(dim, p2)
                clear_Search(grid)
                clear_Path(grid)
                add_valid_fire(grid)
                sa.display_Maze(grid)
                if performStrategyOne(grid, q):
                    successes+=1
            print("Flammability = " + str(q) + ", avg success rate = " + str(float(successes)/trials))
    elif strategy == 2:
        print("Showing Strategy Two Data with dim = " + str(dim) + ", trials per flammability = " + str(trials))
        for prob in range(1,21):
            q = float(prob)/20
            successes = 0
            for x in range(trials):
                grid = generate_Maze(dim, .3)
                while not sa.a_star(grid, 0, 0, dim-1, dim-1):
                    grid = generate_Maze(dim, p2)
                clear_Path(grid)
                clear_Search(grid)
                add_valid_fire(grid)
                sa.display_Maze(grid)
                if performStrategyTwo(grid, q):
                    successes+=1
            print("Flammability = " + str(q) + ", avg success rate = " + str(float(successes)/trials))
    elif strategy == 3:
        print("Showing Strategy Three Data with dim = " + str(dim) + ", trials per flammability = " + str(trials))
        for prob in range(0,21):
            q = float(prob)/20
            successes = 0
            for x in range(trials):
                grid, minDist = add_valid_fire(dim, .3)
                if performStrategyThree(grid, q, minDist):
                    successes+=1
            print("Flammability = " + str(q) + ", avg success rate = " + str(float(successes)/trials))
    else:
        print("Non valid strategy")
        return

#R
#plots the data we got from the collect data functions using matplotlib
def genGraphs(graph):
    prb = []
    for i in range(0, 21):
        prb.append(float(i)/20)
    dfs = [10000, 9942, 9740, 9286, 8447, 7054, 5074, 2412, 190, 0, 0, 0,0,0,0,0,0,0,0,0, 0] #dim =100 trials 10000
    dfs_data = [x / 10000.0 for x in dfs]
    bfs_astar_data= [-1, 13, 60, 141, 270, 432, 536, 312, 14, 0,0,0,0,0,0,0,0,0,0,0, 0] #dim = 100, trials = 1000
    strat1_data = [1, .84, .61, .55, .51, .45, .27, .28, .19, .12, .05, .03, .03, 0,0.02, 0,0,0,0,0,0] #dim = 100, trials = 100
    strat2_data = [1, .96, .91, .83, .57, .53, .42, .32, .26, .16, .04, .02, .02, .01, 0, .01, 0,0,0,0,0] #dim =100 trials = 100
    strat3_data = [1, .93, .94, .81, .74, .57, .59, .41, .33, .16, .12, .05, 0, 0, .01, .01, 0,0,0,0,0] #dim =100 trials = 100

    if int(graph) == 4:
        plt.plot(prb, dfs_data, color= 'c', linewidth = 4.0)
        plt.xlabel("Wall Density")
        plt.ylabel("DFS Success Rate")
        plt.title("DFS Success Rate vs Wall Density")
        plt.show()

    elif int(graph) == 5:
        plt.plot(prb, bfs_astar_data, color= 'm', linewidth = 4.0)
        plt.xlabel("Wall Density")
        plt.ylabel("Average Difference in BFS and A* Nodes Discovered")
        plt.title("Average Difference between BFS and A* Nodes Discovered For Different Wall Densities")
        plt.show()
    elif int(graph) == 1:
        plt.plot(prb, strat1_data, color= 'r', linewidth = 4.0)
        plt.xlabel("Flammability")
        plt.ylabel("Average Success Rate")
        plt.title("Average Success Rate for Strategy One for Different Flammabilities")
        plt.show()
    elif int(graph) == 2:
        plt.plot(prb, strat2_data, color= 'b', linewidth = 4.0)
        plt.xlabel("Flammability")
        plt.ylabel("Average Success Rate")
        plt.title("Average Success Rate for Strategy Two for Different Flammabilities")
        plt.show()

    elif int(graph) ==3:
        plt.plot(prb, strat3_data, color= 'g', linewidth = 4.0)
        plt.xlabel("Flammability")
        plt.ylabel("Average Success Rate")
        plt.title("Average Success Rate for Strategy Three for Different Flammabilities")
        plt.show()

    elif int(graph) == 0:
        plt.plot(prb, strat1_data, color= 'r', linewidth = 4.0, label = "Strategy 1")
        plt.plot(prb, strat2_data, color= 'b', linewidth = 4.0, label = "Strategy 2")
        plt.plot(prb, strat3_data, color= 'g', linewidth = 4.0, label = "Strategy 3")
        plt.xlabel("Flammability")
        plt.ylabel("Average Success Rate")
        plt.title("Average Success Rate for Strategies for Different Flammabilities")
        plt.legend(loc = "upper right")
        plt.ylim(0,1.0)
        plt.show()

#main  area used to run the different functions for different purposes
#usually take in command line arguments to do different things as the following commented code shows

'''if(len(sys.argv) == 2):
    genGraphs(int(sys.argv[1]))
else:
    import searchAlgos as sa
    dim = int(sys.argv[1])
    p2 = float(sys.argv[2])

    fireActive = len(sys.argv) == 4

    if(fireActive):
        q2 = float(sys.argv[3])
    else:
        q2 = 0
    
    grid = generate_Maze(dim, p2)
    sa.display_Maze(grid)
    time.sleep(10)
'''

