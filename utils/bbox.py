from __future__ import annotations
import sys


class BoundingBox:
    
    def __init__(
        self,
        minX: int = sys.maxsize,
        maxX: int = 0.,
        minY: int = sys.maxsize,
        maxY: int = 0.,
    ) -> BoundingBox:
        
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
    
    #union
    def __or__(
        self,
        other: BoundingBox,
    ) -> BoundingBox:
        
        out = BoundingBox(
            minX = min(self.minX, other.minX),
            maxX = max(self.maxX, other.maxX),
            minY = min(self.minY, other.minY),
            maxY = max(self.maxY, other.maxY),
        )
        
        return out
    
    def __ior__(
        self,
        other: BoundingBox,
    ) -> BoundingBox:
        
        self.minX = min(self.minX, other.minX)
        self.maxX = max(self.maxX, other.maxX)
        self.minY = min(self.minY, other.minY)
        self.maxY = max(self.maxY, other.maxY)
        
        return self
        
    def isInside(
        self,
        x: int,
        y: int,
    ) -> bool:
        
        condition = self.minX <= x <= self.maxX and \
                    self.minY <= y <= self.maxY
        
        return condition
    
    def add(
        self,
        x: int,
        y: int,
    ) -> None:
        
        self.minX = min(self.minX, x)
        self.maxX = max(self.maxX, x)
        self.minY = min(self.minY, y)
        self.maxY = max(self.maxY, y)
        
    def __repr__(
        self,
    ) -> str:
        
        return 'x:[%d %d], y:[%d %d]' % (self.minX, self.maxX, self.minY, self.maxY)
    
    