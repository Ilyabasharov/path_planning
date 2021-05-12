# path_planning
Path planning algorithms on grid map

# installation

```bash
pip install -r requirements.txt
```

# description

there are [astar](solver/astar.py), [jps](solver/jps.py), [jpsplus](solver/jpsplus.py), [bbox_pruning](solver/pruning/bbox.py).
ps. pruning algorithm can be applied for each solvers.

# experimental results

[MovingAI](https://movingai.com/benchmarks/grids.html) grid maps were used for experiments. We have chosen two maps [lak307d](https://movingai.com/benchmarks/dao/lak307d.pdf) as easy map and [ost002d](https://movingai.com/benchmarks/dao/ost002d.pdf) as complex map in order to show differences in results.

![](presentation/graphs/error.pdf)
![](presentation/graphs/comparison.pdf)

