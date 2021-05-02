from graph.node import Node

def makePath(
    goal: Node,
) -> tuple:
    
    length = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    
    return path[::-1], length

def getLastEdge(
    goal: Node,
) -> tuple:
    
    current = goal
    prev    = goal
    
    while current.parent:
        prev = current
        current = current.parent
        
    delta = (
        prev.i - current.i,
        prev.j - current.j,
    )
    
    return delta
        