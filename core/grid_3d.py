import random
from core.cell_3d import Cell3D
from core.cell import Cell 
from core.grid import Grid


class Grid3D(Grid):
    @property
    def levels(self):
        return self._levels
    
    def __init__(self, levels: int, rows: int, columns: int):
        self._levels = levels

        super().__init__(rows, columns)

        self.prepare_grid()
        self.configure_cells()

    def prepare_grid(self):
        self._grid = [
            [
                [Cell3D(level, row, column) for column in range(self.columns)]
                for row in range(self.rows)
            ]
            for level in range(self.levels)
        ]

    def configure_cells(self):
        for cell in self.each_cell():
            level = cell.level
            row = cell.row
            column = cell.column
            cell.north = self[level, row - 1, column]
            cell.south = self[level, row + 1, column]
            cell.west = self[level, row, column - 1]
            cell.east = self[level, row, column + 1]
            cell.down = self[level - 1, row, column]
            cell.up = self[level + 1, row, column]

    def __setitem__(self, item, value: Cell3D):
        level, row, column = item
        self.grid[level][row][column] = value

    def __getitem__(self, item):
        level, row, column = item
        if not (0 <= level < self.levels):
            return None
        if not (0 <= row <  self.rows):
            return None
        if not (0 <= column < self.columns):
            return None

        return self.grid[level][row][column]

    def random_cell(self):
        level = random.randrange(0, self.levels)
        row = random.randrange(0, self.rows)
        column = random.randrange(0, self.columns)
        
        return self.grid[level][row][column]

    def size(self):
        return self.levels * self.rows * self.columns

    def each_level(self):
        for level in range(self.levels):
            yield self.grid[level]

    def each_row(self):
        for level in self.each_level():
            for row in level:
                yield row
