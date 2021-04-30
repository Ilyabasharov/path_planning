import re

def readMapFromMovingAIFile(
    path: str,
) -> tuple:
    
    passable = re.compile('[%s]' % ''.join(s for s in ('G', '.', 'S')))
    not_passable = re.compile('[%s]' % ''.join(s for s in ('O', '@', 'T', 'W')))
    
    with open(path, 'r') as file:
        _ = file.readline()
        height = int(file.readline().split('height ')[1])
        width = int(file.readline().split('width ')[1])
        _ = file.readline()
        
        result = re.sub(
            not_passable,
            '#',
            re.sub(
                passable,
                '.',
                file.read()
            ),
        )
        
    return height, width, result

def readTasksFromMovingAIFile(
    path: str,
) -> list:
    
    tasks = []
    with open(path, 'r') as file:
        
        _ = file.readline()
        
        for line in file:
            
            bucket, map_, width, height, jStart, iStart, jGoal, iGoal, optLenght = line.split()
            tasks.append((
                int(width), int(height),
                int(jStart), int(iStart),
                int(jGoal), int(iGoal),
                float(optLenght),
            ))
        
    return tasks