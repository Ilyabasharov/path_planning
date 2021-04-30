from __future__ import annotations

class Map:

    def __init__(
        self: Map,
    ) -> None:
        
        self.width = 0
        self.height = 0
        self.cells = None
        
        self.deltas = [
            (0, 1), (1,  0), (0, -1), (-1,  0),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
        ]
    
    def readFromString(
        self:    Map,
        cellStr: str,
        width:   int,
        height:  int,
    ) -> Map:
        
        self.width = width
        self.height = height
        
        self.cells = [
            [False]*width
            for _ in range(height)
        ]

        i, j = 0, 0
        
        for line in filter(None, cellStr.split('\n')):
            j = 0
            for char in line:
                if char == '.':
                    self.cells[i][j] = False
                elif char == '#':
                    self.cells[i][j] = True
                else:
                    continue
                j += 1
                
            if j != width:
                raise Exception("Size Error. Map width = ", j, ", but must be", width)

            i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)
                    
        return self
                    
    def readFromCells(
        self:      Map,
        width:     int,
        height:    int,
        gridCells: list,
    ) -> Map:
        
        self.width = width
        self.height = height
        self.cells = gridCells
        
        return self
        
    def inBounds(
        self: Map,
        i:    int,
        j:    int,
    ) -> bool:
        
        return 0 <= j < self.width and \
               0 <= i < self.height
    
    def traversable(
        self: Map,
        i:    int,
        j:    int,
        dx:   int,
        dy:   int,
    ) -> bool:
        
        if not self.inBounds(i + dx, j + dy):
            return False
        
        if self.isObstacle(i + dx, j + dy):
            return False
        
        #diag
        if dx != 0 and dy != 0:
            obstacles = self.isObstacle(i,      j + dy) and \
                        self.isObstacle(i + dx, j     )
            
            return not obstacles
        
        return True
    
    def isObstacle(
        self: Map,
        i:    int,
        j:    int,
    ) -> bool:
        
        return self.cells[i][j]
    
    def getAllowedMovements(
        self: Map,
        i:    int,
        j:    int,
    ) -> list:
        
        neighbors = [
            (dx, dy)
            for dx, dy in self.deltas
            if self.traversable(i, j, dx, dy)
        ]
        
        return neighbors