from __future__ import annotations
from types import FunctionType

from solver.base import BaseSolver
from solver.pruning.base import BasePruning

from graph.grid import GridMap
from graph.node import Node

from utils.utils import getDirection


class AStar(BaseSolver):
    
    def __init__(
        self,
        h_func: FunctionType,
        prune:  BasePruning,
    ) -> AStar:
        
        super().__init__(h_func, prune)
        
    def getSuccessors(
        self,
        state: Node,
        goal:  Node,
        grid:  GridMap,
        k:     int,
    ) -> list:
        
        optimal = self.prune.getOptimalDirections(state, goal)
        
        nodes = [
            Node(
                i      = state.i + mv[0],
                j      = state.j + mv[1],
                h      = self.h_func(state.i + mv[0], state.j + mv[1], goal.i, goal.j),
                parent = state,
                k      = k,
            )
            for mv in grid.getAllowedMovements(state.i, state.j)
            if mv in optimal
        ]
        
        return nodes