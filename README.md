# path_planning
Path planning algorithms on grid map

# installation

```bash
pip install -r requirements.txt
```

# description

there are [astar](solver/astar.py), [jps](solver/jps.py), [jpsplus](solver/jpsplus.py), [bbox_pruning](solver/pruning/bbox.py).

all results are described in [jupyter notebook](main.ipynb).

p.s. pruning algorithm can be applied for each solvers.

# routine run

```python
from solver.jpsplus import JPSPlus             #define the solver
from solver.pruning.bbox import BBoxPruning    #define pruning
from utils.distance import diagonalDistance    #define h function
rom solver.base import findPathBase            #define search function
from graph.node import Node                    #define Node for start/finish
from graph.grid import GridMap                 #define occupancy grid map via string
from evaluation.test import simpleTest         #define eval function

startNode  = Node(x_start,  y_start)           #define start Node
finishNode = Node(x_finish, y_finish)          #define finish Node
grid       = GridMap()                         #define grid Map
grid.readFromString(mapstr, width, height)     #see additionals in main.ipynb

#routine run - always call solver.doPreprocess before eval

prune = BBoxPruning()
solver = JPSPlus(diagonalDistance, prune)
solver.doPreprocess(grid)
simpleTest(solver, findPathBase, grid, startNode, goalNode, visualise=True)

```

# experimental results

[MovingAI](https://movingai.com/benchmarks/grids.html) grid maps were used for experiments. We have chosen two maps [lak307d](https://movingai.com/benchmarks/dao/lak307d.pdf) as easy map and [ost002d](https://movingai.com/benchmarks/dao/ost002d.pdf) as complex map in order to show differences in results.

<object data="presentation/graphs/error.pdf" type="application/pdf" width="150px" height="250px">
    <embed src="presentation/graphs/error.pdf" type="application/pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="presentation/graphs/error.pdf">error.pdf</a>.</p>
    </embed>
</object>

<object data="presentation/graphs/comparison.pdf" type="application/pdf" width="150px" height="250px">
    <embed src="presentation/graphs/comparison.pdf" type="application/pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="presentation/graphs/comparison.pdf">comparison.pdf</a>.</p>
    </embed>
</object>

