from __future__ import annotations
from types import FunctionType

from solver.base import BaseSolver
from solver.jps import JPS
from solver.pruning.base import BasePruning

from graph.node import Node
from graph.grid import Map


class JPSPlus(JPS):
    
    def __init__(
        self,
        h_func: FunctionType,
        prune:  BasePruning,
    ) -> JPSPlus:
        
        super().__init__(h_func, prune)
        