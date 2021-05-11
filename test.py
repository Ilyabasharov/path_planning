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
    optLenght: float,
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
    tasks:       list,
    gridMap:     GridMap,
    Hfunction, 
    **args
) -> list:
    
    allTasksResults = {
        'time': [],
        'found': [],
        'length': [],
        'created': []
    }
    
    for task in tqdm.tqdm(tasks):
        width, height, jStart, iStart, jGoal, iGoal, optLenght = [int(el) if i !=6 else float(el) for i, el in enumerate(task)]
        startNode = Node(iStart, jStart)
        goalNode = Node(iGoal, jGoal)
        stats = simpleTest(
            solver, findPathBase, gridMap, startNode, goalNode, optLenght, visualise=False)
        
        allTasksResults['time'].append(stats['time'])
        allTasksResults['found'].append(stats['found'])
        allTasksResults['length'].append(stats['length'])
        allTasksResults['created'].append(stats['created'])



        

    return allTasksResults