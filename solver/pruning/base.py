from __future__ import annotations
from types import FunctionType

from graph.grid import Map
from graph.node import Node


class BasePruning:
    
    def __init__(
        self,
    ) -> BasePrune:
        
        self.preprocessed = False
    
    def preprocess(
        self,
        forcedDirections: FunctionType,
        grid: Map,
    ) -> None:
        
        pass
        
    def getOptimalDirections(
        self,
        state: Node,
        goal:  Node,
    ) -> set:
        
        pass
    

class NoPruning(BasePruning):
    
    def __init__(
        self,
    ) -> NoPruning:
        
        super().__init__()
    
    def preprocess(
        self,
        forcedDirections: FunctionType,
        grid: Map,
    ) -> None:
        
        self.allowed_directions = set(grid.deltas)
        
        self.preprocessed = True
        
    def getOptimalDirections(
        self,
        state: Node,
        goal:  Node,
    ) -> set:
        
        return self.allowed_directions
        