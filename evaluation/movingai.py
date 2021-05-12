from __future__ import annotations
import re
import tqdm
from types import FunctionType

from solver.base import BaseSolver, findPathBase

from graph.grid import GridMap
from graph.node import Node

from container.open import OpenList
from container.closed import ClosedList

from container.base import (
    OpenBase, ClosedBase,
)

from evaluation.test import simpleTest
from solver.pruning.base import BasePruning, NoPruning

from graph.grid import GridMap

from utils.distance import diagonalDistance


class MovingAIDataset:
    
    def __init__(
        self,
        path2map:   str,
        path2tasks: str,
    ) -> MovingAIDataset:
        
        h, w, grid  = self.readMapFromFile(path2map)
        self.map = GridMap().readFromString(grid, w, h)
        self.tasks  = self.readTasksFromFile(path2tasks)
    
    def test(
        self,
        solver:      BaseSolver,
        dist:        FunctionType = diagonalDistance,
        engine:      FunctionType = findPathBase,
        prune:       BasePruning  = NoPruning,
        open_list:   OpenBase     = OpenList,
        closed_list: ClosedBase   = ClosedList,
    ) -> list:
        
        pruning = prune()
        algorithm = solver(dist, pruning)
        
        algorithm.doPreprocess(self.map)
        
        self.result = []
        
        for jStart, iStart, jGoal, iGoal, backet, _ in tqdm.tqdm(self.tasks, desc='Process the tasks'):
            
            startNode = Node(iStart, jStart)
            goalNode = Node(iGoal, jGoal)
        
            stats = simpleTest(algorithm, engine, self.map, startNode, goalNode, backet, visualise=False)
            
            self.result.append(stats)
              
        return self.result
            
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
            
            tasks = []
            
            for line in file:
                bucket, _, _, _, jStart, iStart, jGoal, iGoal, optLength = \
                     line.split()
                
                task = [
                    int(jStart), int(iStart),
                    int(jGoal) , int(iGoal) ,
                    int(bucket),
                    float(optLength),
                ]
                tasks.append(task)
                
        return tasks
    