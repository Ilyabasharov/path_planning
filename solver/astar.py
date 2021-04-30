from __future__ import annotations

from solver.base import BaseSolver
from graph.node import Node
from graph.grid import Map

class AStar(BaseSolver):
    
    def __init__(
        self,
        h_func,
        *args,
    ) -> AStar:
        
        super().__init__(h_func)
        
    def getSuccessors(
        self:  AStar,
        state: Node,
        goal:  Node,
        grid:  Map,
        k:     int,
    ) -> list:
        
        nodes = [
            Node(
                i      = state.i + dx,
                j      = state.j + dy,
                h      = self.h_func(state.i + dx, state.j + dy, goal.i, goal.j),
                parent = state,
                k      = k,
            )
            for (dx, dy) in grid.getAllowedMovements(state.i, state.j)
        ]
        
        return nodes