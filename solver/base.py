from __future__ import annotations

from container.base import (
    OpenBase,
    ClosedBase,
)

from graph.node import Node
from graph.grid import Map


class BaseSolver:
    
    def __init__(
        self: BaseSolver,
        h_func,
    ) -> None:
        
        self.h_func = h_func
        
    def getSuccessors(
        self:          BaseSolver,
        current_state: Node,
        goal_state:    Node,
        grid_map:      Map,
        *args,
    ) -> list:
        
        pass
    

def findPathBase(
    solver:     BaseSolver,
    gridMap:    Map,
    start:      tuple,
    finish:     tuple,
    openType:   OpenBase,
    closedType: ClosedBase,
) -> tuple:
    
    k = 0
    
    openList   = openType()
    closedList = closedType()
    
    goalNode = Node(
        i=finish[0], j=finish[1],
        h=0, k=k,
    )
    startNode = Node(
        i=start[0], j=start[1],
        h=solver.h_func(
            start[0], start[1], finish[0], finish[1],
        ), k=k,
    )
    
    openList.addNode(startNode)
    
    while not openList.isEmpty():
        
        currentNode = openList.getBestNode()
        closedList.addNode(currentNode)
        
        if currentNode == goalNode:
            return (True, currentNode, closedList, openList)
        
        for tempNode in solver.getSuccessors(currentNode, goalNode, gridMap, k):
            if not closedList.wasExpanded(tempNode):
                openList.addNode(tempNode)
                
        k += 1
        
    return (False, None, closedList, openList)