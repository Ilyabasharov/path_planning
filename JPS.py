from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import math
from utils import Map, Open, Closed, Node, CalculateCost,  DiagonalDistance

def GetDirection(state, parent):
  dx = int(math.copysign(1, state[0] - parent[0]))
  dy = int(math.copysign(1, state[1] - parent[1]))

  if state[0] - parent[0] == 0:
    dx = 0
  
  if state[1] - parent[1] == 0:
    dy = 0

  return dx, dy

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
    return (X, Y)

  if not traversable((X, Y), 0, 0, cells):
    return None

  if dx != 0 and dy != 0:
    while True:
      if CheckJumpPoint((x,y), dx, dy, cells):
        return (x, y)

      if (GetJumpPoint((x,y), dx, 0, goal, cells) is not None or GetJumpPoint((x,y), 0, dy, goal, cells) is not None):
        return (x, y)

      x += dx
      y += dy

      if x == goal[0] and y == goal[1]:
        return (x, y)

      if not traversable((x,y), 0, 0, cells):
        return None

      if cells[x - dx][y] == 1 and cells[x][y - dy] == 1:
        return None

  elif dx != 0:
    while True:
      if CheckJumpPoint((x,Y), dx, 0, cells):
        return (x, Y)

      x += dx

      if not traversable((x,Y), 0, 0, cells):
        return None

      if x == goal[0] and Y == goal[1]:
        return (x, Y)
  else:
    while True:
      if CheckJumpPoint((X,y), 0, dy, cells):
        return (X, y)

      y += dy

      if not traversable((X,y), 0, 0, cells):
        return None

      if X == goal[0] and y == goal[1]:
        return (X, y)

  return jump(X, Y, dx, dy, goal, cells)

          
  
def traversable(state, dx, dy, cells):
  x0 = state[0]
  y0 = state[1]

  x = x0 + dx
  y = y0 + dy

  if x < 0 or y < 0 or x >= cells.shape[0] or y >= cells.shape[1]:
    return False

  if dx != 0 and dy != 0:
    if (cells[x][y0] == 1 and cells[x0][y] == 1) or cells[x][y] == 1:
      return False

  else:
    if cells[x][y] == 1:
      return False

  return True


def GetNeighbours(state, parent, cells):
  
  neighbours = []
  if parent is None:
    delta = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    for d in delta:
        if traversable(state, d[0], d[1], cells):
          
          neighbours.append((state[0] + d[0], state[1] + d[1]))

    return neighbours
  
  dx, dy = GetDirection(state, parent)
  if dx != 0 and dy != 0:
    if traversable(state, 0, dy, cells):
      neighbours.append((state[0], state[1] + dy))
    if traversable(state, dx, 0, cells):
      neighbours.append((state[0] + dx, state[1]))
    if (traversable(state, 0, dy, cells) or traversable(state, dx, 0, cells) ) and traversable(state, dx, dy, cells):
      neighbours.append((state[0] + dx, state[1] + dy))

    if not traversable(state, -dx, 0, cells) and traversable(state, 0, dy, cells):
      neighbours.append((state[0] - dx, state[1] + dy))

    if not traversable(state, 0, -dy, cells) and traversable(state, dx, 0, cells):
      neighbours.append((state[0] + dx, state[1] - dy))

  else:
    if dx == 0:
      if traversable(state, 0, dy, cells):
        neighbours.append((state[0], state[1] + dy))
      if not traversable(state, 1, 0, cells):
        neighbours.append((state[0] + 1, state[1] + dy))
      if not traversable(state, -1, 0, cells):
        neighbours.append((state[0] - 1, state[1] + dy))

    else:
      if traversable(state, dx, 0, cells):
        neighbours.append((state[0] + dx, state[1]))
      if not traversable(state, 0, 1, cells):
        neighbours.append((state[0] + dx, state[1] + 1))
      if not traversable(state, 0, -1, cells):
        neighbours.append((state[0] + dx, state[1] - 1))        
  return neighbours

def GetSuccessors(state, parent, goal, cells):
  successors = []

  neighbours = GetNeighbours(state, parent, cells)

  for s in neighbours:
    dx, dy = s[0] - state[0], s[1] - state[1]
    jp = GetJumpPoint(state, dx, dy, goal, cells)
    if jp is not None:
      successors.append(jp)

  return successors

def JPS(gridMap : Map, iStart : int, jStart : int, iGoal : int, jGoal : int, heuristicFunction = DiagonalDistance):
    
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

        for s_ in GetSuccessors((s.i, s.j), parent,  (iGoal, jGoal), np.array(gridMap.cells)):
            if not CLOSED.WasExpanded(Node(s_[0], s_[1])):
                OPEN.AddNode(Node(s_[0], s_[1], g = s.g + CalculateCost(s_[0], s_[1], s.i, s.j), k = k,  h = heuristicFunction(s_[0], s_[1], iGoal, jGoal), parent = s ))
        k +=1

    return False, None, CLOSED, OPEN