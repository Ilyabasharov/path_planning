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