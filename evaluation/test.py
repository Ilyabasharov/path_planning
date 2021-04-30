import time

from solver.base import BaseSolver
from graph.grid import Map
from graph.node import Node
from container.base import (
    OpenBase,
    ClosedBase,
)

from utils.path import makePath
from utils.visualisation import drawResult


def simpleTest(
    searcher: BaseSolver,
    engine,
    task: str,
    height: int, width: int,
    iStart: int, jStart: int,
    iGoal: int, jGoal: int,
    open_list:   OpenBase,
    closed_list: ClosedBase,
    visualise: bool=True,
) -> dict:
    
    taskMap = Map().readFromString(task, width, height)
    
    start = (iStart, jStart)
    goal  = (iGoal , jGoal )
    
    stats = {
        'time':    None,
        'found':   False,
        'length':  None,
        'created': 0,
    }
    
    start_time = time.time()
    
    found, last_node, closed_list, open_list = engine(
        searcher,
        taskMap,
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
            drawResult(taskMap, start, goal, path, closed_list, open_list)
    
    return stats