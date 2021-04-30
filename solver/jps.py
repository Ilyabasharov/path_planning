from __future__ import annotations

from solver.base import BaseSolver
from graph.node import Node
from graph.grid import Map

from solver.utils import getDirection


class JPS(BaseSolver):
    
    def __init__(
        self: JPS,
        h_func,
        *args,
    ) -> JPS:
        
        super().__init__(h_func)
        
    def getSuccessors(
        self:  JPS,
        state: Node,
        goal:  Node,
        grid:  Map,
        k:     int,
    ) -> list:
        
        disallowed = self.getDisallowedDirections(state)
        
        successors = [
            self.getJumpPoint(state.i, state.j, delta[0], delta[1], goal, grid)
            for delta in grid.getAllowedMovements(state.i, state.j)
            if delta not in disallowed
        ]
        
        nodes = [
            Node(
                i      = successor[0],
                j      = successor[1],
                h      = self.h_func(successor[0], successor[1], goal.i, goal.j),
                parent = state,
                k      = k,
            )
            for successor in successors
            if successor is not None
        ]
        
        return nodes
            
    def getDisallowedDirections(
        self:  JPS,
        state: Node,
        *args,
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
        self: JPS,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: Map,
    ) -> bool:
        
        down = grid.traversable(i, j, -dx, +dy) and not grid.traversable(i, j, -dx,   0)
        up   = grid.traversable(i, j, +dx, -dy) and not grid.traversable(i, j,   0, -dy)
        
        return up or down
    
    def isVerticalJumpPoint(
        self: JPS,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: Map,
    ) -> bool:
        
        up   = grid.traversable(i, j, dx, +1) and not grid.traversable(i, j, 0, +1)
        down = grid.traversable(i, j, dx, -1) and not grid.traversable(i, j, 0, -1)
        
        return up or down
    
    def isHorisontalJumpPoint(
        self: JPS,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        grid: Map,
    ) -> bool:
        
        up   = grid.traversable(i, j, +1, dy) and not grid.traversable(i, j, +1, 0)
        down = grid.traversable(i, j, -1, dy) and not grid.traversable(i, j, -1, 0)
        
        return up or down
    
    def getJumpPoint(
        self: JPS,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
        goal: Node,
        grid: Map,
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
