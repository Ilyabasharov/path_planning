from __future__ import annotations
import itertools
import collections
from types import FunctionType

from solver.base import BaseSolver
from solver.jps import JPS
from solver.pruning.base import BasePruning

from graph.node import Node
from graph.grid import GridMap

from utils.utils import getDirection


class JPSPlus(JPS):
    
    def __init__(
        self,
        h_func: FunctionType,
        prune:  BasePruning,
    ) -> JPSPlus:
        
        super().__init__(h_func, prune)
        
    def addXdim2Goal_(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        p_i:  int,
        p_j:  int,
        g_i:  int,
        g_j:  int,
        data: list,
    ) -> bool:
        
        if (i - g_i) * (p_i - g_i) <= 0:
            x = g_i
            y = (g_i - p_i) * dx * dy + p_j
            
            point = (x, y)
            if x == g_i and y == g_j:
                data.append(point)
                return True
            
            to_goal = getDirection(g_i, g_j, x, y)
                    
            if to_goal in self.jump_points[point]:
                check_x, check_y = self.jump_points[point][to_goal]

                if abs(check_y - y) >= abs(g_j - y):
                    data.append(point)
                    return False
                
        return None
    
    def addYdim2Goal_(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        p_i:  int,
        p_j:  int,
        g_i:  int,
        g_j:  int,
        data: list,
    ) -> bool:
        
        if (j - g_j) * (p_j - g_j) <= 0:
            x = (g_j - p_j) * dx * dy + p_i
            y = g_j
            
            point = (x, y)
            if x == g_i and y == g_j:
                data.append(point)
                return True
            
            to_goal = getDirection(g_i, g_j, x, y)
                    
            if to_goal in self.jump_points[point]:
                check_x, check_y = self.jump_points[point][to_goal]

                if abs(check_x - x) >= abs(g_i - x):
                    data.append(point)
                    return False
                
        return None

    def filteredSuccessors(
        self,
        state: Node,
        goal:  Node,
        grid:  GridMap,
    ) -> list: 
        
        optimal = self.prune.getOptimalDirections(state, goal)
        allow = self.getAllowedDirections(state)
        
        recommend = optimal - allow
        
        current = (state.i, state.j)
        
        base_successors = [
            (self.jump_points[current][edge], edge)
            for edge in self.jump_points[current]
            if edge in recommend
        ]
            
        forced_successors = []
        
        for (i, j), (dx, dy) in base_successors:
                
             #diag
            if dx != 0 and dy != 0:
                
                if self.addXdim2Goal_(i, j, dx, dy, state.i, state.j, goal.i, goal.j, forced_successors) or \
                   self.addYdim2Goal_(i, j, dx, dy, state.i, state.j, goal.i, goal.j, forced_successors):
                    break
                    
            #horisontal
            elif dx == 0:
                if self.addYdim2Goal_(i, j, dx, dy, state.i, state.j, goal.i, goal.j, forced_successors):
                    break
                    
            else:
                if self.addXdim2Goal_(i, j, dx, dy, state.i, state.j, goal.i, goal.j, forced_successors):
                    break
                        
            forced_successors.append((i, j))
                
        return forced_successors
        
    def getJumpPoint(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: GridMap,
    ) -> tuple:
        
        if not grid.traversable(i, j, dx, dy):
            return (i, j), False
        
        x, y = i + dx, j + dy
        
        while True:
            
            if self.checkJumpPoint(x, y, dx, dy, grid):
                return (x, y), True
            
            #diag
            if dx != 0 and dy != 0:
                for e_dx, e_dy in [(dx, 0), (0, dy)]:
                    if self.getJumpPoint(x, y, e_dx, e_dy, grid)[1]:
                        return (x, y), True
                    
            if not grid.traversable(x, y, dx, dy):
                return (x, y), False

            x += dx
            y += dy
        
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
        
        self.jump_points = collections.defaultdict(dict)
        
        for node in itertools.product(range(grid.height), range(grid.width)):
            
            if grid.isObstacle(node[0], node[1]):
                continue
                
            for edge in grid.getAllowedMovements(node[0], node[1]):
                
                jp, _ = self.getJumpPoint(node[0], node[1], edge[0], edge[1], grid)
                
                if jp is not None:
                    self.jump_points[node][edge] = jp
        
