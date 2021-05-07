import itertools
from PIL import (
    Image, ImageDraw,
)
from IPython.display import display

from container.base import (
    OpenBase, ClosedBase,
)

from graph.node import Node
from graph.grid import GridMap


def drawResult(
    grid:        GridMap,
    start:       Node        = None,
    goal:        Node        = None,
    path:        list        = None,
    closed_list: ClosedBase  = None,
    open_list:   OpenBase    = None,
    draw_cost:   bool        = False,
) -> None:
    
    def getRectangle(
        i: int,
        j: int,
        k: int,
    ) -> list:
        
        return [j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1]
    
    k    = 40
    hIm  = grid.height * k
    wIm  = grid.width * k
    im   = Image.new('RGB', (wIm, hIm), color = 'white')
    draw = ImageDraw.Draw(im)
    
    for i, j in itertools.product(range(grid.height), range(grid.width)):
        if grid.isObstacle(i, j):
            draw.rectangle(
                xy   = getRectangle(i, j, k),
                fill = (70, 80, 80),
            )
                
    for container, color in zip((open_list,       closed_list    ),
                                ((213, 219, 219), (131, 145, 146))):
        if container is not None:
            for node in container:
                draw.rectangle(
                    xy    =  getRectangle(node.i, node.j, k),
                    fill  = color,
                    width = 0,
                )
                
    if draw_cost:
        for node in nodesExpanded:
            coord = getRectangle(node.i, node.j, k)
            draw.text(
                xy    = ((coord[0] + coord[2]) // 2, (coord[1] + coord[3]) // 2),
                text  = '%.1f' % (node.g),
                fill  = (231, 76, 60),
            )

    if path is not None:
        for node in path:
            draw.rectangle(
                xy    = getRectangle(node.i, node.j, k),
                fill  = (52, 152, 219) if not grid.isObstacle(node.i, node.j) else (230, 126, 34),
                width = 0,
            )
                    
    for keypoint, color in zip((start,         goal         ),
                               ((40, 180, 99), (231, 76, 60))):

        if keypoint is not None and not grid.isObstacle(keypoint.i, keypoint.j):
            draw.rectangle(
                xy    = getRectangle(keypoint.i, keypoint.j, k),
                fill  = color, 
                width = 0,
            )
    
    display(im)