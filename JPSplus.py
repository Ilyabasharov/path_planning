from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import math
from utils import Map, Open, Closed, Node, CalculateCost,  DiagonalDistance



def CheckJumpPoint(state, dx, dy, cells):
  if dx != 0 and dy != 0:
    if ((traversable(state, -dx, dy, cells) and not traversable(state, -dx, 0, cells)) or 
        (traversable(state, dx, -dy, cells) and not traversable(state, 0, -dy, cells))):
      return True
  elif dx != 0:
    if ((traversable(state, dx, 1, cells) and not traversable(state, 0, 1, cells)) or 
        (traversable(state, dx, -1, cells) and not traversable(state, 0, -1, cells))):
      return True
  else:
    if ((traversable(state, 1, dy, cells) and not traversable(state, 1, 0, cells)) or 
        (traversable(state, -1, dy, cells) and not traversable(state, -1, 0, cells))):
      return True 

def GetJumpPoint(state, dx, dy, goal, cells):
  X, Y = state[0] + dx, state[1] + dy
  x, y = X, Y

  if X == goal[0] and Y == goal[1]:
    return (X, Y), True

  if not traversable((X, Y), 0, 0, cells) or cells[x - dx][y] == 1 and cells[x][y - dy] == 1:
    return (x-dx, y-dy), False

  if dx != 0 and dy != 0:
    while True:
      if CheckJumpPoint((x,y), dx, dy, cells):
        return (x, y), True

      if (GetJumpPoint((x,y), dx, 0, goal, cells)[1] or GetJumpPoint((x,y), 0, dy, goal, cells)[1]):
        return (x, y), True

      x += dx
      y += dy

      if x == goal[0] and y == goal[1]:
        return (x, y), True

      if not traversable((x,y), 0, 0, cells):
        return (x-dx, y-dy), False

      if cells[x - dx][y] == 1 and cells[x][y - dy] == 1:
        return (x-dx, y-dy), False

  elif dx != 0:
    while True:
      if CheckJumpPoint((x,Y), dx, 0, cells):
        return (x, Y), True

      x += dx

      if not traversable((x,Y), 0, 0, cells):
        return (x-dx, Y), False

      if x == goal[0] and Y == goal[1]:
        return (x, Y), True
  else:
    while True:
      if CheckJumpPoint((X,y), 0, dy, cells):
        return (X, y), True

      y += dy

      if not traversable((X,y), 0, 0, cells):
        return (X, y-dy), False

      if X == goal[0] and y == goal[1]:
        return (X, y), True

  return GetJumpPoint(X, Y, dx, dy, goal, cells)
          
  
def traversable(state, dx, dy, cells):
  x0 = state[0]
  y0 = state[1]

  x = x0 + dx
  y = y0 + dy

  if x0 < 0 or y0 < 0 or x0 >= cells.shape[0] or y0 >= cells.shape[1]:
    return False

  if x < 0 or y < 0 or x >= cells.shape[0] or y >= cells.shape[1]:
    return False

  if dx != 0 and dy != 0:
    if (cells[x][y0] == 1 and cells[x0][y] == 1) or cells[x][y] == 1:
      return False

  else:
    if cells[x][y] == 1:
      return False

  return True


def ProcessMap(cells):
    proc_map = {}
    delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    for i in range(len(cells)):
        for j in range(len(cells[0])):
            if cells[i][j] == 1:
                continue
            else:
                val = []
                for d in delta:
                    dx, dy = d[0], d[1]
                    jp = GetJumpPoint((i,j), dx, dy, (-100, -100), cells)[0]
                    val.append(jp)
                proc_map[(i, j)] = val
    return proc_map

def GetDirection(state, parent):
  delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
  dx = int(math.copysign(1, state[0] - parent[0]))
  dy = int(math.copysign(1, state[1] - parent[1]))

  if state[0] - parent[0] == 0:
    dx = 0
  
  if state[1] - parent[1] == 0:
    dy = 0
  return delta.index([dx, dy]), (dx, dy)

def GetNeighbours(state, parent, proc_map):
  delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
  all_neighbours = proc_map[state]
  neighbours = []
  dx, dy = GetDirection(parent, state)[1]
  if dx != 0 and dy != 0:
      neighbours.append(all_neighbours[delta.index([-dx, -dy])])
      neighbours.append(all_neighbours[delta.index([0, -dy])])
      neighbours.append(all_neighbours[delta.index([-dx, 0])])

  if dx != 0 and dy == 0:
      neighbours.append(all_neighbours[delta.index([-dx, 0])])
      neighbours.append(all_neighbours[delta.index([-dx, 1])])
      neighbours.append(all_neighbours[delta.index([-dx, -1])])
      neighbours.append(all_neighbours[delta.index([0, -1])])
      neighbours.append(all_neighbours[delta.index([0, 1])])
  
  if dx == 0 and dy != 0:
      neighbours.append(all_neighbours[delta.index([0, -dy])])
      neighbours.append(all_neighbours[delta.index([1, -dy])])
      neighbours.append(all_neighbours[delta.index([-1, -dy])])
      neighbours.append(all_neighbours[delta.index([-1, 0])])
      neighbours.append(all_neighbours[delta.index([1, 0])])

  return neighbours
  

def GetSuccessors(state, parent, goal, cells, proc_map):
  successors = []
  '''
  if parent is not None:
    neighbours = GetNeighbours(state, parent, proc_map)
  else:
    neighbours = proc_map[state]
  '''
  neighbours = proc_map[state]
  for d, s in enumerate(neighbours):
    if s is None or s == state:
        continue
    
    index = GetDirection(s, state)[0]
    dx, dy = GetDirection(s, state)[1]

    if dx != 0 and dy != 0:
        if (s[0] - goal[0]) * (state[0] - goal[0]) <= 0: 
            x = goal[0]
            y = (goal[0] - state[0]) * dx * dy + state[1]
            if (x,y) == goal:
              successors.append(goal)
              break
            
            if abs(proc_map[(x,y)][GetDirection(goal, (x,y))[0]][1] - y) >= abs(goal[1] - y):
                successors.append((x, y))   
                continue
            
        if (s[1] - goal[1]) * (state[1] - goal[1]) <= 0: 
            x = state[0] + (goal[1] - state[1]) * dx * dy
            y = goal[1]
            if (x,y) == goal:
              successors.append(goal)
              break
            
            if abs(proc_map[(x,y)][GetDirection(goal, (x,y))[0]][0] - x) >= abs(goal[0] - x) :
                successors.append((x, y))
                continue             
            
    if dx != 0 and dy == 0:
        if (s[0] - goal[0]) * (state[0] - goal[0]) <= 0:
            x = goal[0]
            y = state[1]
            if (x,y) == goal:
              successors.append(goal)
              break
            
            if abs(proc_map[(x,y)][GetDirection(goal, (x,y))[0]][1] - y) >= abs(goal[1] - y) :
                successors.append((x, y))
                continue   
            
    if dy != 0 and dx == 0:
        if (s[1] - goal[1]) * (state[1] - goal[1]) <= 0: 
            x = state[0]
            y = goal[1]
            if (x,y) == goal:
              successors.append(goal)
              break
            
            if abs(proc_map[(x,y)][GetDirection(goal, (x,y))[0]][0] - x) >= abs(goal[0] - x):
                successors.append((x, y))
                continue
     
    successors.append((s[0], s[1]))
    
  return successors

def JPSplus(gridMap : Map, iStart : int, jStart : int, iGoal : int, jGoal : int, *args, heuristicFunction = DiagonalDistance):
    map_proc = args[0]
    OPEN = Open()
    k = 1
    start = Node(iStart, jStart, g = 0, h = heuristicFunction(iStart, jStart, iGoal, jGoal))
    OPEN.AddNode(start)
    CLOSED = Closed()
    while not OPEN.isEmpty():
        s = OPEN.GetBestNode()
        CLOSED.AddNode(s)
        if s.i == iGoal and s.j == jGoal:
            return (True, s, CLOSED, OPEN)

        if s.parent is not None:
          parent = (s.parent.i, s.parent.j)
        else:
          parent = None

        for s_ in GetSuccessors((s.i, s.j), parent,  (iGoal, jGoal), np.array(gridMap.cells), map_proc):
            if not CLOSED.WasExpanded(Node(s_[0], s_[1])):
                OPEN.AddNode(Node(s_[0], s_[1], g = s.g + CalculateCost(s_[0], s_[1], s.i, s.j), k = k,  h = heuristicFunction(s_[0], s_[1], iGoal, jGoal), parent = s ))
        k +=1

    return False, None, CLOSED, OPEN