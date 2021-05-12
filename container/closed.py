from __future__ import annotations

from container.base import ClosedBase
from graph.node import Node

class ClosedList(ClosedBase):

    def __init__(
        self,
    ) -> ClosedList:
        
        super().__init__()
        
        self.elements_set  = set()

    def __iter__(
        self,
    ) -> iter:
        
        return iter(self.elements_set)
    
    def __len__(
        self,
    ) -> int:
        
        return len(self.elements_set)
    
    def addNode(
        self,
        item: Node,
    ) -> None:
        
        self.elements_set.add(item)

    def wasExpanded(
        self,
        item: Node,
    ) -> bool:
        
        return item in self.elements_set