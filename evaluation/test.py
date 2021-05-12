import time
from types import FunctionType

from solver.base import BaseSolver, findPathBase

from graph.grid import GridMap
from graph.node import Node

from container.base import (
    OpenBase, ClosedBase,
)
from container.open import OpenList
from container.closed import ClosedList

from utils.visualisation import drawResult
from utils.path import makePath


def simpleTest(
    solver:      BaseSolver,
    engine:      FunctionType,
    grid:        GridMap,
    start:       Node,
    goal:        Node,
    open_list:   OpenBase   = OpenList,
    closed_list: ClosedBase = ClosedList,
    complexity:  int        = 0,
    visualise:   bool       = True,
) -> dict:
    
    stats = {
        'time':    None,
        'found':   False,
        'length':  None,
        'created': 0,
        'complex': complexity,
    }
    
    start_time = time.perf_counter()
    
    found, last_node, closed_nodes, open_nodes = engine(
        solver, grid, start, goal,
    )
    
    stats['time']    = time.perf_counter() - start_time
    stats['found']   = found
    stats['created'] = len(closed_nodes) + len(open_nodes)
    
    if found:
        stats['length'] = last_node.g
        
    if visualise:
        path = makePath(last_node)
        drawResult(grid, start, goal, path, closed_nodes, open_nodes)
    
    return stats