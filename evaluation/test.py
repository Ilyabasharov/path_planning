import time
from types import FunctionType

from solver.base import BaseSolver
from solver.base import findPathBase
from solver.pruning.base import BasePruning

from graph.grid import Map
from graph.node import Node
from container.base import (
    OpenBase,
    ClosedBase,
)

from container.open import OpenList
from container.closed import ClosedList

from utils.path import makePath
from utils.visualisation import drawResult


def simpleTest(
    solver:      BaseSolver,
    pruning:     BasePruning,
    engine:      FunctionType,
    grid:        Map,
    start:       Node,
    goal:        Node,
    open_list:   OpenBase   = OpenList,
    closed_list: ClosedBase = ClosedList,
    visualise:   bool       = True,
) -> dict:
    
    stats = {
        'time':    None,
        'found':   False,
        'length':  None,
        'created': 0,
    }
    
    if not pruning.preprocessed:
        pruning.preprocess(solver.getForsedDirections, grid)
    
    start_time = time.time()
    
    found, last_node, closed_list, open_list = engine(
        solver,
        grid,
        start,
        goal,
        open_list,
        closed_list,
    )
    
    stats['time']    = time.time() - start_time
    stats['found']   = found
    stats['created'] = len(closed_list) + len(open_list)
    
    if found:
        
        path, length = makePath(last_node)
        
        stats['length'] = length
        
        if visualise:
            drawResult(grid, start, goal, path, closed_list, open_list)
    
    return stats