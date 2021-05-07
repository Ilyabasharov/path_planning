from __future__ import annotations

from graph.node import Node

class OpenBase:
    
    def __init__(
        self,
        *args,
    ) -> OpenBase:
        
        pass
    
    def __iter__(
        self,
    ) -> iter:
        
        pass
    
    def __len__(
        self,
    ) -> int:
        
        pass
    
    def isEmpty(
        self,
    ) -> bool:
        
        return len(self) == 0
    
    def addNode(
        self,
        item: Node,
    ) -> None:
        
        pass
    
    def getBestNode(
        self,
    ) -> Node:
        
        pass
    
    
class ClosedBase:
    
    def __init__(
        self,
    ) -> ClosedBase:
        
        pass
    
    def __iter__(
        self,
    ) -> iter:
        
        pass
    
    def __len__(
        self,
    ) -> int:
        
        pass
    
    def addNode(
        self,
        item: Node,
    ) -> None:
        
        pass
    
    def wasExpanded(
        self,
        item: Node,
    ) -> bool:
        
        pass
    