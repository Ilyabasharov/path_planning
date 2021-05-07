import time
import tqdm
from types import FunctionType

from solver.base import BaseSolver, findPathBase
from solver.pruning.base import BasePruning

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
    visualise:   bool       = True,
) -> dict:
    
    stats = {
        'time':    None,
        'found':   False,
        'length':  None,
        'created': 0,
    }
    
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

def massiveTest(
    solver:      BaseSolver, 
    tasks,
    stringMap,
    Hfunction, 
    **args
) -> list:
    
    allTasksResults = []
    
    for task in tqdm.tqdm(tasks):
        width, height, jStart, iStart, jGoal, iGoal, optLenght = task
        pathDiff, nNodes, nSteps, correct = SimpleTest(
            SearchFunction, height, width, stringMap, iStart, jStart, iGoal, jGoal, optLenght, False, biderect, **args)
        
        allTasksResults.append((pathDiff, nNodes, nSteps, correct, optLenght))
        

    return allTasksResults