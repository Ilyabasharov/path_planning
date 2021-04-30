from __future__ import annotations

from graph.node import Node

class OpenBase:
    
    def __init__(
        self: OpenBase,
        *args,
    ) -> None:
        
        pass
    
    def __iter__(
        self: OpenBase,
    ) -> iter:
        
        pass
    
    def __len__(
        self: OpenBase,
    ) -> int:
        
        pass
    
    def isEmpty(
        self: OpenBase,
    ) -> bool:
        
        return len(self) == 0
    
    def addNode(
        self: OpenBase,
        item: Node,
    ) -> None:
        
        pass
    
    def getBestNode(
        self: OpenBase,
    ) -> Node:
        
        pass
    
    
class ClosedBase:
    
    def __init__(
        self: ClosedBase,
    ) -> None:
        
        pass
    
    def __iter__(
        self: ClosedBase,
    ) -> iter:
        
        pass
    
    def __len__(
        self: ClosedBase,
    ) -> int:
        
        pass
    
    def addNode(
        self: ClosedBase,
        item: Node,
    ) -> None:
        
        pass
    
    def wasExpanded(
        self: ClosedBase,
        item: Node,
    ) -> bool:
        
        pass
    