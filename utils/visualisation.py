from PIL import (
    Image,
    ImageDraw,
)

from IPython.display import display

from graph.grid import Map
from graph.node import Node

def drawResult(
    gridMap: Map,
    start:   tuple = None,
    goal:    tuple = None,
    path:    list = None,
    nodesExpanded = None,
    nodesOpened   = None,
) -> None:
    
    def getRectangle(
        i: int,
        j: int,
        k: int,
    ) -> list:
        
        return [j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1]
    
    k    = 20
    hIm  = gridMap.height * k
    wIm  = gridMap.width * k
    im   = Image.new('RGB', (wIm, hIm), color = 'white')
    draw = ImageDraw.Draw(im)
    
    for i in range(gridMap.height):
        for j in range(gridMap.width):
            if gridMap.isObstacle(i, j):
                draw.rectangle(
                    xy   = getRectangle(i, j, k),
                    fill = (70, 80, 80),
                )
                
    for container, color in zip((nodesOpened,     nodesExpanded  ),
                                ((213, 219, 219), (131, 145, 146))):
        if container is not None:
            for node in container:
                draw.rectangle(
                    xy    =  getRectangle(node.i, node.j, k),
                    fill  = color,
                    width = 0,
                )

    if path is not None:
        for node in filter(None, path):
            draw.rectangle(
                xy    = getRectangle(node.i, node.j, k),
                fill  = (52, 152, 219) if not gridMap.isObstacle(node.i, node.j) else (230, 126, 34),
                width = 0,
            )
                    
    for keypoint, color in zip((start,         goal         ),
                               ((40, 180, 99), (231, 76, 60))):

        if keypoint is not None and not gridMap.isObstacle(keypoint[0], keypoint[1]):
            draw.rectangle(
                xy    = getRectangle(keypoint[0], keypoint[1], k),
                fill  = color, 
                width = 0,
            )
    
    display(im)