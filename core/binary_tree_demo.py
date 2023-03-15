from grid import Grid
from binary_tree import BinaryTree

grid = Grid(6, 6)
BinaryTree.on(grid)
grid.to_png().save("grid_image.png", "PNG", optimize=True)
print(grid)