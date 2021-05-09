def signOfDifference(
    diff: int,
) -> int:
    
    sign = diff and 1 - 2 * (diff < 0)
    
    return sign

def getDirection(
    i1: int,
    j1: int,
    i2: int, 
    j2: int,
) -> tuple:
    
    direction = (
        signOfDifference(i1 - i2), 
        signOfDifference(j1 - j2),
    )
    
    return direction