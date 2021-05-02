import math

CHV = 1.
CD = math.sqrt(2)


def manhattanDistance(
    i1: int,
    j1: int,
    i2: int, 
    j2: int
) -> float:
    
    dx, dy = abs(i1 - i2), abs(j1 - j2)
    
    return CHV*(dx + dy)


def diagonalDistance(
    i1: int,
    j1: int,
    i2: int,
    j2: int
) -> float:
    
    dx, dy = abs(i1 - i2), abs(j1 - j2)
    
    return CHV*abs(dx - dy) + CD*min(dx, dy)


def chebyshevDistance(
    i1: int,
    j1: int,
    i2: int,
    j2: int
) -> float:
    
    dx, dy = abs(i1 - i2), abs(j1 - j2)
    
    return CHV*max(dx, dy)


def euclidDistance(
    i1: int,
    j1: int,
    i2: int,
    j2: int
) -> float:
    
    dx, dy = abs(i1 - i2), abs(j1 - j2)
    
    return CHV*math.sqrt(dx*dx + dy*dy)

def zeroDistance(
    i1: int,
    j1: int,
    i2: int,
    j2: int
) -> float:
    
    return 0.