from heapq import heappop, heappush
from PIL import Image, ImageDraw
import numpy as np
import os
import matplotlib.pyplot as plt
import math
EPS = 0.000001

class Map:

    # Default constructor
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = []
    
    # Initialization of map by string.
    def ReadFromString(self, cellStr, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for _ in range(width)] for _ in range(height)]
        cellLines = cellStr.split("\n")
        i = 0
        j = 0
        for l in cellLines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self.cells[i][j] = 0
                    elif c == '#':
                        self.cells[i][j] = 1
                    else:
                        continue
                    j += 1
                # TODO
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width )
                
                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height )
    
    # Initialization of map by list of cells.
    def SetGridCells(self, width, height, gridCells):
        self.width = width
        self.height = height
        self.cells = gridCells

    # Checks cell is on grid.
    def inBounds(self, i, j):
        return (0 <= j < self.width) and (0 <= i < self.height)
    
    # Checks cell is not obstacle.
    def Traversable(self, i, j):
        return not self.cells[i][j]

    # Creates a list of neighbour cells as (i,j) tuples.
    def GetNeighbors(self, i, j):
        # TODO Change the function so that the list includes the diagonal neighbors of the cell.
        # Cutting corners must be prohibited
        neighbors = []

        delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]

        for d in delta:
            if abs(d[0]) == abs(d[1]):
                if self.inBounds(i + d[0], j + d[1]):
                    if self.Traversable(i + d[0], j) and self.Traversable(i, j + d[1]) and self.Traversable(i + d[0], j + d[1]):
                        neighbors.append((i + d[0], j + d[1]))

            elif abs(d[0]) != abs(d[1]):
                if self.inBounds(i + d[0], j + d[1]):
                    if self.Traversable(i + d[0], j + d[1]):
                        neighbors.append((i + d[0], j + d[1]))
 

        return neighbors

def CalculateCost(i1, j1, i2, j2):
    return math.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)

class Node:
    def __init__(self, i = -1, j = -1, g = 0, h = 0, F = None, Fhatch = None,parent = None, k =0):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        self.k = k
        
        if F is None:
            self.F = self.g + h
        else:
            self.F = F        
        self.parent = parent
    
    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)

    def __lt__(self, other):
        return self.F < other.F or ((self.F == other.F) and (self.h < other.h)) \
            or ((self.F == other.F) and (self.h == other.h) and (self.k > other.k))

class Open:
    def __init__(self):
        self.prioritizedQueue = []
        self.ij_to_node = {}

    def __iter__(self):
        return iter(self.ij_to_node.values())

    def __len__(self):
        return len(self.ij_to_node)

    def isEmpty(self):
        return len(self.ij_to_node) == 0

    def AddNode(self, item : Node):
        
        ij = item.i, item.j
        oldNode = self.ij_to_node.get(ij)
        if oldNode is None or item.g < oldNode.g:
            self.ij_to_node[ij] = item
            heappush(self.prioritizedQueue, item)

    def GetBestNode(self):
        bestNode = heappop(self.prioritizedQueue)
        ij = bestNode.i, bestNode.j
        while self.ij_to_node.pop(ij, None) is None:
            bestNode = heappop(self.prioritizedQueue)
            ij = bestNode.i, bestNode.j
        return bestNode

class Closed:

    
    def __init__(self):
        self.elements = []
        self.set = set()
        self.count = 0

    def __iter__(self):
        return iter(self.elements)
    
    def __len__(self):
        return self.count
    
    # AddNode is the method that inserts the node to CLOSED
    def AddNode(self, item : Node, *args):
        self.set.add((item.i, item.j))
        self.elements.append(item)
        self.count += 1

    # WasExpanded is the method that checks if a node has been expanded
    def WasExpanded(self, item : Node, *args):
        return (item.i, item.j) in self.set

def DiagonalDistance(i1, j1, i2, j2):
    dx = abs(int(i1) - int(i2))
    dy = abs(int(j1) - int(j2))

    return dx + dy + ( np.sqrt(2) - 2 ) * min(dx, dy)

def MakePath(goal):
    length = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length

def DiagonalDistance(i1, j1, i2, j2):
    dx = abs(int(i1) - int(i2))
    dy = abs(int(j1) - int(j2))

    return dx + dy + ( np.sqrt(2) - 2 ) * min(dx, dy)

def Draw(gridMap : Map, start : Node = None, goal : Node = None, path : list = None, nodesExpanded = None, nodesOpened = None):
    k = 5
    hIm = gridMap.height * k
    wIm = gridMap.width * k
    im = Image.new('RGB', (wIm, hIm), color = 'white')
    draw = ImageDraw.Draw(im)
    for i in range(gridMap.height):
        for j in range(gridMap.width):
            if(gridMap.cells[i][j] == 1):
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=( 70, 80, 80 ))

    if nodesOpened is not None:
        for node in nodesOpened:
            draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1), fill=(213, 219, 219), width=0)

    if nodesExpanded is not None:
        for node in nodesExpanded:
            draw.rectangle((node.j * k, node.i * k, (node.j + 1) * k - 1, (node.i + 1) * k - 1), fill=( 131, 145, 146 ), width=0)

    if path is not None:
        for step in path:
            if (step is not None):
                if (gridMap.Traversable(step.i, step.j)):
                    draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1), fill=(52, 152, 219), width=0)
                else:
                    draw.rectangle((step.j * k, step.i * k, (step.j + 1) * k - 1, (step.i + 1) * k - 1), fill=(230, 126, 34), width=0)

    if (start is not None) and (gridMap.Traversable(start.i, start.j)):
        draw.rectangle((start.j * k, start.i * k, (start.j + 1) * k - 1, (start.i + 1) * k - 1), fill=(40, 180, 99), width=0)
    
    if (goal is not None) and (gridMap.Traversable(goal.i, goal.j)):
        draw.rectangle((goal.j * k, goal.i * k, (goal.j + 1) * k - 1, (goal.i + 1) * k - 1), fill=(231, 76, 60), width=0)


    fig, ax = plt.subplots(dpi=150)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.imshow(np.asarray(im))

def ReadMapFromMovingAIFile(fileName):
    path = "DragonAge/maps/" + fileName
    mapFile = open(path)
    t = mapFile.readline().split()[1]
    height = int(mapFile.readline().split()[1])
    width = int(mapFile.readline().split()[1])
    _ = mapFile.readline()
    cells = [[0 for _ in range(width)] for _ in range(height)]
    i = 0
    j = 0
    for l in mapFile:
        j = 0
        for c in l:
            if c == '.' or c == 'G' or c == 'S':
                cells[i][j] = 0
            elif c == 'O' or c == "@" or c == "T" or c == "W" :
                cells[i][j] = 1
            else:
            
                continue
            
            j += 1
            
        if j != width:
            raise Exception("Size Error. Map width = ", j, ", but must be", width, "(map line: ", i, ")")
                
        i += 1
        if(i == height):
            break

    return (width, height, cells)  


def ReadTaskFromMovingAIFile(fileName):
    path = "DragonAge/tasks/" + fileName
    tasksFile = open(path)
    
    list_iStart = []
    list_jStart = []
    list_iGoal = []
    list_jGoal = []
    list_length = []
    for i, line in enumerate(tasksFile.readlines()):
        if i == 0:
            continue
        list_tasks = line.split()
        
        list_iStart.append(int(list_tasks[5]))
        list_jStart.append(int(list_tasks[4]))
        list_iGoal.append(int(list_tasks[7]))
        list_jGoal.append(int(list_tasks[6]))
        list_length.append(float(list_tasks[8]))    



    return (list_iStart, list_jStart, list_iGoal, list_jGoal, list_length)

def SimpleTest(SearchFunction, height, width, mapstr, iStart, jStart, iGoal, jGoal, pathLen, *args):
    taskMap = Map()
    taskMap.ReadFromString(mapstr, width, height)
    start = Node(iStart, jStart)
    goal = Node(iGoal, jGoal)

    try:
        result = SearchFunction(taskMap, start.i, start.j, goal.i, goal.j, *args)
        nodesExpanded = result[2]
        nodesOpened = result[3]
        
        if result[0]:
            path = MakePath(result[1])
            correct = abs(path[1] - pathLen) < EPS
            Draw(taskMap, start, goal, path[0], nodesExpanded, nodesOpened)
            print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
        else:
            print("Path not found!")
    except Exception as e:
        print("Execution error")
        print(e)

def MassiveTest(SearchFunction, proc_maps, taskFileName, mapFileName, max_task=600, heuristicFunction = DiagonalDistance):
    stat = dict()
    stat["corr"] = []
    stat["len"] = []
    stat["nc"] = []
    stat["st"] = []
    
    taskMap = Map()
    width, height, cells = ReadMapFromMovingAIFile(mapFileName)
    taskMap.SetGridCells(width,height,cells)
    list_iStart, list_jStart, list_iGoal, list_jGoal, list_length = ReadTaskFromMovingAIFile(taskFileName)
    assert len(list_iStart) == len(list_jStart) == len(list_iGoal) == len(list_jGoal)
    task_count = 0
    for i in range(len(list_iStart)):
        if task_count > max_task:
            break
        iStart = list_iStart[i]
        jStart = list_jStart[i]
        iGoal = list_iGoal[i]
        jGoal = list_jGoal[i]
        length = list_length[i]
        proc_map = proc_maps[::-1].pop()
        try:

            result = SearchFunction(taskMap, iStart, jStart, iGoal, jGoal,proc_map, heuristicFunction)
            nodesExpanded = result[2]
            nodesOpened = result[3]
            if result[0]:
                path = MakePath(result[1]) 
                stat["len"].append(path[1])
                correct = abs(path[1] - length) < EPS
                stat["corr"].append(correct)
                
                print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
                print(path[1], length)
            else:
                print("Path not found!")
                stat["corr"].append(False)
                stat["len"].append(0.0)

            stat["nc"].append(len(nodesOpened) + len(nodesExpanded))
            stat["st"].append(len(nodesExpanded))

        except Exception as e:
            print("Execution error")
            print(e)

    return stat