

from random import choice
from grid import Grid

class BinaryTree:
    @classmethod
    def on(cls, grid: Grid):
        for cell in grid.each_cell():
            neighbours = []
            cell.north and neighbours.append(cell.north)
            cell.east and neighbours.append(cell.east)
            
            # print(cell.north, cell.south, cell.east, cell.west)
            if len(neighbours) > 0:
                neighbour = choice(neighbours)
                neighbour and cell.link(neighbour)
            
        return grid