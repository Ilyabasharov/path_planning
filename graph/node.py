from __future__ import annotations

from utils.distance import euclidDistance


class Node:
    
    def __init__(
        self:   Node,
        i:      int,
        j:      int,
        h:      int,
        parent: Node = None,
        k:      int  = 0,
    ) -> None:
        
        self.i = i
        self.j = j
        
        if parent is not None:
            self.g = parent.g + euclidDistance(parent.i, parent.j, i, j)
        else:
            self.g = 0
        
        self.h = h
        self.k = k

        self.f = self.g + self.h
        self.parent = parent
    
    def __eq__(
        self:  Node,
        other: Node,
    ) -> bool:
        
        if isinstance(other, (tuple, list)):
            return self.i == other[0] and \
                   self.j == other[1]
        
        return self.i == other.i and \
               self.j == other.j
        

    def __lt__(
        self:  Node,
        other: Node,
    ) -> bool:
        
        return (self.f <  other.f) \
            or (self.f == other.f and self.h <  other.h) \
            or (self.f == other.f and self.h == other.h and self.k > other.k)
