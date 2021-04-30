from __future__ import annotations

from container.base import ClosedBase
from graph.node import Node

class ClosedList(ClosedBase):

    def __init__(
        self: ClosedList,
    ) -> None:
        
        super().__init__()
        
        self.elements_set  = set()
        self.elements_list = list()

    def __iter__(
        self: ClosedList,
    ) -> iter:
        
        return iter(self.elements_list)
    
    def __len__(
        self: ClosedList,
    ) -> int:
        
        return len(self.elements_list)
    
    def addNode(
        self: ClosedList,
        item: Node,
    ) -> None:
        
        self.elements_set.add((item.i, item.j))
        self.elements_list.append(item)

    def wasExpanded(
        self: ClosedList,
        item: Node,
    ) -> bool:
        
        return (item.i, item.j) in self.elements_set