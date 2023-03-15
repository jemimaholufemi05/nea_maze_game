from core.cell import Cell
from random import randrange

class Grid:
    
    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns

    @property
    def size(self) -> int:
        return self.rows * self.columns
    
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        
        self.grid = self.prepare_grid()
        self.configure_cells()
    
    def __setitem__(self, item, value: Cell):
        row, column = item
        self.grid[row][column] = value
        
    def __getitem__(self, item):
        row, column = item
        if not (0 <= row < self.rows):
            return None
        if not (0 <= column < self.columns):
            return None
        
        return self.grid[row][column]

    def prepare_grid(self):
        return [ 
            [ Cell(row, column) for column in range(self.columns) ] for row in range(self.rows) 
        ]
                
    def each_cell(self):
        for row in self.each_row():
            for cell in row:
                yield cell
    
    def each_row(self):
        for row in range(self.rows):
            yield self.grid[row]
            
    
    def configure_cells(self):
        for cell in self.each_cell():
            row = cell.row
            column = cell.column
            
            cell.north = self[row - 1, column]
            cell.south = self[row + 1, column]
            cell.east = self[row, column + 1]
            cell.west = self[row, column - 1]
            
    def random_cell(self):
        row = randrange(0, self.rows)
        column = randrange(0, self.columns)
        return self[row, column]
    
    def __str__(self):
        output = "+" + "---+" * self.columns + "\n"
        
        for row in self.each_row():
            top = " " if row[0].row == 0 and row[0].column == 0 else "|" 
            bottom = "+"
            
            for cell in row:
                if not(cell):
                    cell = Cell(-1, -1)
        
                body = "   " # <-- that's THREE (3) spaces!
                east_boundary = " " if cell.is_linked(cell.east) else "|"
                top += body + east_boundary
                
                # three spaces below, too >>-------------->> >...<
                south_boundary = "   " if cell.is_linked(cell.south) else "---"
                corner = "+"
                
                bottom += south_boundary + corner
                
            
            output += top + "\n"
            output += bottom + "\n"
            
        return output
                
                
        
