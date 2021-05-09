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
            directions |= {
                (dx, dy),
                (dx,  0),
                ( 0, dy),
            }
        
        #horisontal
        elif dx == 0:
            directions |= {
                (dx, dy),
                (+1,  0),
                (-1,  0),
                (+1, dy),
                (-1, dy),
            }
        #vertical
        else:
            directions |= {
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
        
        base_x, base_y = i + dx, j + dy
        
        if (base_x, base_y) == goal:
            return (base_x, base_y)
        
        x, y = base_x, base_y
        
        #diag
        if dx != 0 and dy != 0:
            
            while True:
                if self.isDiagonalJumpPoint(x, y, dx, dy, grid):
                    return (x, y)
                
                if self.getJumpPoint(x, y, dx,  0, goal, grid) is not None or \
                   self.getJumpPoint(x, y,  0, dy, goal, grid) is not None :
                    return (x, y)
                
                if not grid.traversable(x, y, dx, dy):
                    return None
                
                x += dx
                y += dy
                
                if (x, y) == goal:
                    return (x, y)
        #horisontal
        elif dx == 0:
            
            while True:
                if self.isHorisontalJumpPoint(base_x, y, dx, dy, grid):
                    return (base_x, y)
                
                if not grid.traversable(base_x, y, dx, dy):
                    return None
                
                y += dy
                
                if (base_x, y) == goal:
                    return (base_x, y)
        #vertical       
        else:
            
            while True:
                if self.isVerticalJumpPoint(x, base_y, dx, dy, grid):
                    return (x, base_y)
                
                if not grid.traversable(x, base_y, dx, dy):
                    return None
                
                x += dx
                
                if (x, base_y) == goal:
                    return (x, base_y)
                
    def getForsedDirections(
        self,
        iState: int,
        jState: int,
        dx:     int,
        dy:     int,
        grid:   GridMap,
    ) -> list:
        
        forced = []
        
         #diag
        if dx != 0 and dy != 0:
            
            for e_dx, e_dy in [(dx, 0), (0, dy)]:
                
                if grid.traversable(iState, jState, e_dx, e_dy):
                    forced.append((e_dx, e_dy))
                
                f_dx = dx - 2*e_dx
                f_dy = dy - 2*e_dy
                
                if not grid.traversable(iState, jState, -e_dx, -e_dy) \
                   and grid.traversable(iState, jState, +f_dx, +f_dy):
                    
                    forced.append((f_dx, f_dy))
                    
        #horisontal
        elif dx == 0:
            
            for e_dx in [1, -1]:
                
                if not grid.traversable(iState, jState, e_dx, +0) \
                   and grid.traversable(iState, jState, e_dx, dy):
                    
                    forced.append((e_dx, dy))
                    
         #vertical
        else:
            
            for e_dy in [1, -1]:
                
                if not grid.traversable(iState, jState, +0, e_dy) \
                   and grid.traversable(iState, jState, dx, e_dy):
                    
                    forced.append((dx, e_dy))
                    
        return forced
            