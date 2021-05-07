from __future__ import annotations

import itertools
import collections
from types import FunctionType

from solver.pruning.base import BasePruning
from solver.base import dijkstraFloodFill
from utils.bbox import BoundingBox
from utils.path import getLastEdge
from graph.grid import GridMap


class BBoxPruning(BasePruning):
    
    def __init__(
        self,
    ) -> BBoxPruning:
        
        super().__init__()
        
        self.bboxes = collections.defaultdict(dict)
        
    def preprocess(
        self,
        forcedDirections: FunctionType,
        grid:             GridMap,
    ) -> None:
        
        per_x, per_y = range(grid.height), range(grid.width)
        
        # init the data
        for i, j in itertools.product(per_x, per_y):
            
            node = (i, j)
            
            if grid.isObstacle(i, j):
                continue

            for edge in grid.getAllowedMovements(i, j):

                self.bboxes[node][edge] = BoundingBox()
                    
        # find unions of bboxes
        for i, j in itertools.product(per_x, per_y):
            
            node = (i, j)
            
            if grid.isObstacle(i, j):
                continue
            
            forced_directions = collections.defaultdict(set)
            
            for computed_node in dijkstraFloodFill(grid, node):
                
                dx, dy = getLastEdge(computed_node)
                
                edge = (dx, dy)
                    
                self.bboxes[node][edge].add(computed_node.i, computed_node.j)
                
                forced_directions[edge].update(forcedDirections(i, j, dx, dy, grid))
            
            for edge in forced_directions:
                for forced in forced_directions[edge]:
                    self.bboxes[node][edge] |= self.bboxes[node][forced]
                
        self.preprocessed = True
        
    def getOptimalDirections(
        self,
        state: Node,
        goal:  Node,
    ) -> set:
        
        current = (state.i, state.j)
        
        optimal = {
            direction
            for direction in self.bboxes[current]
            if self.bboxes[current][direction].isInside(goal.i, goal.j)
        }
        
        return optimal