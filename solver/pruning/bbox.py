from __future__ import annotations
import tqdm
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
        verbose:          bool = True,
    ) -> None:
        
        per_x, per_y = range(grid.height), range(grid.width)
        
        #init the data
        self.bboxes = {
            node: {
                edge: BoundingBox()
                for edge in grid.getAllowedMovements(node[0], node[1])
            }
            
            for node in itertools.product(per_x, per_y)
            if not grid.isObstacle(node[0], node[1])
        }
        
        if verbose:
            iterator = tqdm.tqdm(
                iterable = itertools.product(per_x, per_y),
                total    = grid.height*grid.width,
                desc     = 'Preprocess the map',
                leave    = True,
            )
        else:
            iterator = itertools.product(per_x, per_y)
            
                    
        # find unions of bboxes
        for node in iterator:
            
            if grid.isObstacle(node[0], node[1]):
                continue
            
            forced_directions = collections.defaultdict(set)
            
            for computed_node in dijkstraFloodFill(grid, node):
                
                edge = getLastEdge(computed_node)
                    
                self.bboxes[node][edge].add(computed_node.i, computed_node.j)
                
                forced_directions[edge].update(forcedDirections(node[0], node[1], edge[0], edge[1], grid))
            
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