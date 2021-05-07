from __future__ import annotations
from heapq import (
    heappop,
    heappush,
)

from container.base import OpenBase
from graph.node import Node

class OpenList(OpenBase):
    
    def __init__(
        self,
    ) -> OpenList:
        
        super().__init__()
        
        self.prioritizedQueue = []
        self.ij_to_node = {}

    def __iter__(
        self,
    ) -> iter:
        
        return iter(self.ij_to_node.values())

    def __len__(
        self,
    ) -> int:
        
        return len(self.ij_to_node)

    def addNode(
        self,
        item: Node,
    ) -> None:
        
        ij = item.i, item.j
        oldNode = self.ij_to_node.get(ij, None)
        
        if oldNode is None or item.g < oldNode.g:
            self.ij_to_node[ij] = item
            heappush(self.prioritizedQueue, item)

    def getBestNode(
        self,
    ) -> Node:
        
        bestNode = heappop(self.prioritizedQueue)
        ij = bestNode.i, bestNode.j
        
        while self.ij_to_node.pop(ij, None) is None:
            bestNode = heappop(self.prioritizedQueue)
            ij = bestNode.i, bestNode.j
            
        return bestNode