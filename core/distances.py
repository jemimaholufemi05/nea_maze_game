class Distances:
    def __init__(self, root):
        self.root = root
        self.cells = {}
        self.cells[self.root] = 0
    
    def dist(self, cell):
        return self.cells[cell]
    
    def dist(self, cell, distance):
        self.cells[cell] = distance
        
    def cells(self):
        return self.cells.keys()
    from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from core.cell import Cell
else:
    Cell = "Cell"

def is_cell(cell: Cell) -> bool:
    return type(cell).__name__ == Cell
class Distances:

    def __init__(self, root: Cell) -> None:
        if not is_cell(root):
            raise ValueError("Root must be a cell")

        self.root: Cell = root
        self._cells: List[Cell] = dict()
        self._cells[root] = 0

    def __getitem__(self, cell: Cell) -> Optional[int]:
        if not is_cell(cell):
            raise IndexError("Distances must be indexed with a cell")

        if cell in self._cells.keys():
            return self._cells[cell]
        return None

    def __setitem__(self, cell: Cell, distance: int) -> None:
        if not is_cell(cell):
            raise IndexError("Distances must be indexed with a cell")

        self._cells[cell] = distance

    @property
    def cells(self) -> List[Cell]:
        return list(self._cells.keys())

    @property
    def max(self) -> Tuple[Cell, int]:
        max_distance = 0
        max_cell = self.root

        for cell in self._cells:
            if self._cells[cell] > max_distance:
                max_cell = cell
                max_distance = self._cells[cell]

        return max_cell, max_distance

    def path_to(self, destination: Cell) -> "Distances":
        """
        Traverses backwards, from destination to root/origin
        """
        if not is_cell(destination):
            raise ValueError("Destination must be a cell")

        current_cell = destination

        breadcrumbs = Distances(self.root)
        breadcrumbs[current_cell] = self._cells[current_cell]

        while current_cell != self.root:
            for neighbor in current_cell.links:
                if self._cells[neighbor] < self._cells[current_cell]:
                    breadcrumbs[neighbor] = self._cells[neighbor]
                    current_cell = neighbor
                    break

        return breadcrumbs


def is_cell(cell: Cell) -> bool:
    return type(cell).__name__ == Cell

    def path_to(self, goal):
        current = goal
        
        breadcrumbs = Distances(self.root)
        breadcrumbs.dist(self.cells[current])
        
        while not current = self.root:
            for neighbour in current.links:
                if self.cells[neighbour] = self.cells[current]:
                    breadcrumbs.dist