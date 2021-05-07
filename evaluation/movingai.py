from __future__ import annotations
import re

class MovingAIDataset:
    
    def __init__(
        self,
        path2map:   str,
        path2tasks: str,
    ) -> MovingAIDataset:
        
        h, w, grid  = self.readMapFromFile(path2map)
        self.tasks  = self.readTasksFromFile(path2tasks)
        
    def readMapFromFile(
        self,
        path: str,
    ) -> tuple:
        
        passable = re.compile('[%s]' % ''.join(s for s in ('G', '.', 'S')))
        not_passable = re.compile('[%s]' % ''.join(s for s in ('O', '@', 'T', 'W')))

        with open(path, 'r') as file:
            _ = file.readline()
            height = int(file.readline().split('height ')[1])
            width = int(file.readline().split('width ')[1])
            _ = file.readline()

            grid = re.sub(
                not_passable,
                '#',
                re.sub(
                    passable,
                    '.',
                    file.read()
                ),
            )

        return height, width, grid
    
    def readTasksFromFile(
        self,
        path: str,
    ) -> list:
        
        tasks = []
        
        with open(path, 'r') as file:
        
            _ = file.readline()
            
            tasks = [
                line.split()
                for line in file
            ]
        
                
        return tasks
    