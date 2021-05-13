from __future__ import annotations
from types import FunctionType

from solver.base import BaseSolver
from solver.pruning.base import BasePruning

from graph.grid import GridMap
from graph.node import Node

from utils.utils import getDirection


class JPS(BaseSolver):
    
    def __init__(
        self,
        h_func: FunctionType,
        prune:  BasePruning,
    ) -> JPS:
        
        super().__init__(h_func, prune)
        
    def getSuccessors(
        self,
        state: Node,
        goal:  Node,
        grid:  GridMap,
        k:     int,
    ) -> list:
        
        nodes = [
            Node(
                i      = i,
                j      = j,
                h      = self.h_func(i, j, goal.i, goal.j),
                parent = state,
                k      = k,
            )
            for i, j in filter(None, self.filteredSuccessors(state, goal, grid))
        ]
        
        return nodes
    
    def filteredSuccessors(
        self,
        state: Node,
        goal:  Node,
        grid:  GridMap,
    ) -> list:
        
        optimal = self.prune.getOptimalDirections(state, goal)
        allow = self.getAllowedDirections(state)
        
        recommend = optimal - allow
        
        successors = [
            self.getJumpPoint(state.i, state.j, delta[0], delta[1], goal, grid)
            for delta in grid.getAllowedMovements(state.i, state.j)
            if delta in recommend
        ]
        
        return successors
            
    def getAllowedDirections(
        self,
        state: Node,
    ) -> set:
        
        directions = set()
        parent = state.parent
        
        if parent is None:
            return directions
        
        dx, dy = getDirection(parent.i, parent.j, state.i, state.j)
        
        #diag
        if dx != 0 and dy != 0:
            directions = {
                (dx, dy),
                (dx,  0),
                ( 0, dy),
            }
        
        #horisontal
        elif dx == 0:
            directions = {
                (dx, dy),
                (+1,  0),
                (-1,  0),
                (+1, dy),
                (-1, dy),
            }
        #vertical
        else:
            directions = {
                (dx, dy),
                ( 0, +1),
                ( 0, -1),
                (dx, +1),
                (dx, -1),
            }
            
        return directions
    
    def isDiagonalJumpPoint(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: GridMap,
    ) -> bool:
        
        down = grid.traversable(i, j, -dx, +dy) and not grid.traversable(i, j, -dx,   0)
        up   = grid.traversable(i, j, +dx, -dy) and not grid.traversable(i, j,   0, -dy)
        
        return up or down
    
    def isVerticalJumpPoint(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: GridMap,
    ) -> bool:
        
        up   = grid.traversable(i, j, dx, +1) and not grid.traversable(i, j, 0, +1)
        down = grid.traversable(i, j, dx, -1) and not grid.traversable(i, j, 0, -1)
        
        return up or down
    
    def isHorisontalJumpPoint(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: GridMap,
    ) -> bool:
        
        up   = grid.traversable(i, j, +1, dy) and not grid.traversable(i, j, +1, 0)
        down = grid.traversable(i, j, -1, dy) and not grid.traversable(i, j, -1, 0)
        
        return up or down
    
    def getJumpPoint(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        goal: Node,
        grid: GridMap,
    ) -> tuple:
        
        if not grid.traversable(i, j, dx, dy):
            return None
        
        x, y = i + dx, j + dy
        
        if x == goal.i and y == goal.j:
            return x, y
        
        while True:
            
            if self.checkJumpPoint(x, y, dx, dy, grid):
                return x, y
            
            #diag
            if dx != 0 and dy != 0:
                for e_dx, e_dy in [(dx, 0), (0, dy)]:
                    if self.getJumpPoint(x, y, e_dx, e_dy, goal, grid) is not None:
                        return x, y
                    
            if not grid.traversable(x, y, dx, dy):
                return None

            x += dx
            y += dy
            
            if x == goal.i and y == goal.j:
                return x, y
                
    def checkJumpPoint(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: GridMap,
    ) -> list:
        
        if dx != 0 and dy != 0:
            return self.isDiagonalJumpPoint(i, j, dx, dy, grid)
        
        elif dx == 0:
            return self.isHorisontalJumpPoint(i, j, dx, dy, grid)
        
        elif dy == 0:
            return self.isVerticalJumpPoint(i, j, dx, dy, grid)
                    
        return False
    
                
    def getForsedDirections(
        self,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: GridMap,
    ) -> list:
        
        forced = []
        
         #diag
        if dx != 0 and dy != 0:
            
            for edge in [(dx, 0), (0, dy)]:
                
                if grid.traversable(i, j, edge[0], edge[1]):
                    forced.append(edge)
                
                f_edge = (dx - 2*edge[0], dy - 2*edge[1])
                
                if not grid.traversable(i, j, -edge[0],   -edge[1]  ) \
                   and grid.traversable(i, j, +f_edge[0], +f_edge[1]):
                    
                    forced.append(f_edge)
                    
        #horisontal
        elif dx == 0:
            
            for e_dx in [1, -1]:
                
                if not grid.traversable(i, j, e_dx, +0) \
                   and grid.traversable(i, j, e_dx, dy):
                    
                    forced.append((e_dx, dy))
                    
         #vertical
        else:
            
            for e_dy in [1, -1]:
                
                if not grid.traversable(i, j, +0, e_dy) \
                   and grid.traversable(i, j, dx, e_dy):
                    
                    forced.append((dx, e_dy))
                    
        return forced
            
