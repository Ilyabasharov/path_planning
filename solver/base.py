from __future__ import annotations
from types import FunctionType

from container.base import (
    OpenBase,
    ClosedBase,
)

from container.open import OpenList
from container.closed import ClosedList

from graph.node import Node
from graph.grid import Map

from solver.pruning.base import (
    BasePruning,
    NoPruning,
)


class BaseSolver:
    
    def __init__(
        self,
        h_func: FunctionType,
        prune:  BasePruning,
    ) -> BaseSolver:
        
        self.h_func = h_func
        self.prune  = prune
        
    def getSuccessors(
        self,
        current_state: Node,
        goal_state:    Node,
        grid_map:      Map,
        **kwargs,
    ) -> list:
        
        pass
    
    def getForsedDirections(
        self,
        iState: int,
        jState: int,
        dx:     int,
        dy:     int,
        grid:   Map,
    ) -> list:
        
        pass
    

def findPathBase(
    solver:     BaseSolver,
    gridMap:    Map,
    startNode:  Node,
    goalNode:   Node,
    openType:   OpenBase   = OpenList,
    closedType: ClosedBase = ClosedList,
) -> tuple:
    
    k = 0
    
    openList   = openType()
    closedList = closedType()
    
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


def dijkstraFloodFill(
    gridMap:    Map,
    start:      tuple,
    openType:   OpenBase   = OpenList,
    closedType: ClosedBase = ClosedList,
) -> tuple:
    
    k = 0
    
    openList   = openType()
    closedList = closedType()
    
    startNode = Node(
        i=start[0], j=start[1],
        h=0, k=k,
    )
    
    for (dx, dy) in gridMap.getAllowedMovements(startNode.i, startNode.j):
        tempNode = Node(
                i      = startNode.i + dx,
                j      = startNode.j + dy,
                h      = 0.,
                parent = startNode,
            )
        openList.addNode(tempNode)
    
    while not openList.isEmpty():
        
        currentNode = openList.getBestNode()
        closedList.addNode(currentNode)
        
        for (dx, dy) in gridMap.getAllowedMovements(currentNode.i, currentNode.j):
            tempNode = Node(
                i      = currentNode.i + dx,
                j      = currentNode.j + dy,
                h      = 0.,
                parent = currentNode,
                k      = k
            )
            if not closedList.wasExpanded(tempNode):
                openList.addNode(tempNode)
                
        k += 1
                
    return closedList