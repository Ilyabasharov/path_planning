from __future__ import annotations
import itertools
from types import FunctionType

from solver.base import BaseSolver
from solver.jps import JPS
from solver.pruning.base import BasePruning

from graph.node import Node
from graph.grid import GridMap


class JPSPlus(JPS):
    
    def __init__(
        self,
        h_func: FunctionType,
        prune:  BasePruning,
    ) -> JPSPlus:
        
        super().__init__(h_func, prune)
    
    def filteredSuccessors(
        self,
        state: Node,
        goal:  Node,
        grid:  GridMap,
    ) -> list: 
        
        optimal = self.prune.getOptimalDirections(state, goal)
        diallow = self.getDisallowedDirections(state)
        
        recommend = optimal - diallow
        
        successors = []
        
        current = (state.i, state.j)
        
        for edge in self.jump_points[current]:
            
            if edge not in recommend:
                continue
            
            point = self.jump_points[current][edge]
                
            if point is None:
                continue
                
            i, j = point
                
            if (i - goal.i) * (state.i - goal.i) <= 0 and \
               (j - goal.j) * (state.j - goal.j) <= 0:
                
                successors.append((goal.i, goal.j))
                break

            if (i - goal.i) * (state.i - goal.i) <= 0:
                if not grid.isObstacle(goal.i, j):
                    successors.append((goal.i, j))

            if (j - goal.j) * (state.j - goal.j) <= 0:
                if not grid.isObstacle(i, goal.j):
                    successors.append((i, goal.j))
            
            if (i - goal.i) * (state.i - goal.i) > 0 and \
               (j - goal.j) * (state.j - goal.j) > 0:
                successors.append((i, j))
                
        return successors
        
    def getJumpPoint(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: GridMap,
    ) -> tuple:
        
        if not grid.traversable(i, j, dx, dy):
            return None, False
        
        base_x, base_y = i + dx, j + dy
        
        x, y = base_x, base_y
        
        #diag
        if dx != 0 and dy != 0:
            
            while True:
                if self.isDiagonalJumpPoint(x, y, dx, dy, grid):
                    return (x, y), True
                
                if self.getJumpPoint(x, y, dx,  0, grid)[1] or \
                   self.getJumpPoint(x, y,  0, dy, grid)[1] :
                    return (x, y), True
                
                if not grid.traversable(x, y, dx, dy):
                    return (x, y), False
                
                x += dx
                y += dy
                
        #horisontal
        elif dx == 0:
            
            while True:
                if self.isHorisontalJumpPoint(base_x, y, dx, dy, grid):
                    return (base_x, y), True
                
                if not grid.traversable(base_x, y, dx, dy):
                    return (base_x, y), False
                
                y += dy
                
        #vertical       
        else:
            
            while True:
                if self.isVerticalJumpPoint(x, base_y, dx, dy, grid):
                    return (x, base_y), True
                
                if not grid.traversable(x, base_y, dx, dy):
                    return (x, base_y), False
                
                x += dx
        
    def doPreprocess(
        self,
        grid: GridMap,
    ) -> None:
        
        if not self.preprocessed:
            self.prune.preprocess(self.getForsedDirections, grid)
            self.computeJumpPoints(grid)
        
        self.preprocessed = True
            
    def computeJumpPoints(
        self,
        grid: GridMap,
    ) -> None:
                
        self.jump_points = {
            
            (i, j): {
                (dx, dy): self.getJumpPoint(i, j, dx, dy, grid)[0]
                for dx, dy in grid.getAllowedMovements(i, j)
            }
            
            for i, j in itertools.product(range(grid.height), range(grid.width))
            if not grid.isObstacle(i, j)
        }
        