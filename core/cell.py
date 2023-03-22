from typing import Any, cast, Dict, Hashable, List, Optional

from core.distances import Distances

class Cell:
       
    @property
    def row(self):
        return self._row
    
    @property
    def column(self):
        return self._column
    
    @property
    def north(self):
        return self._north
    
    @north.setter
    def north(self, north):
        self._north = north
        
    @property
    def south(self):
        return self._south
    
    @south.setter
    def south(self, south):
        self._south = south
    
    @property
    def east(self):
        return self._east
    
    @east.setter
    def east(self, east):
        self._east = east
        
    @property
    def west(self):
        return self._west
    
    @west.setter
    def west(self, west):
        self._west = west
 
    def __init__(self, row: int, column: int):
        self._row = row
        self._column = column
        self._east = None
        self._west = None
        self._south = None
        self._north = None
        self.links = {}
    
    def link(self, cell, bidi=True) -> 'Cell':
        self.links[cell] = True
        bidi and cell.link(self, bidi=False)
        
        return self
    
    
    def unlink(self, cell, bidi=True) -> 'Cell':
        del self.links[cell]
        bidi and cell.unlink(self, False)
        return self
    
    
    def links(self):
        return list(self.links.keys())
    
    
    def is_linked(self, cell: "Cell") -> bool:
        return cell in self.links.keys()
    
    @property
    def neighbours(self):
        list = []
        self.north and list.append(self.north)
        self.south and list.append(self.south)
        self.east and list.append(self.east)
        self.west and list.append(self.west)
        return list
    
    @property
    def distances(self) -> Distances:
        distances = Distances(self)
        frontier = [self]

        while len(frontier) > 0:
            new_frontier = []
            for cell in frontier:
                for linked_cell in cell.links:
                    if distances[linked_cell] is None and distances[cell] is not None:
                        distances[linked_cell] = cast(int, distances[cell]) + 1
                        new_frontier.append(linked_cell)
            frontier = new_frontier

        return distances

    
    def __eq__(self, other_cell: Optional["Cell"]) -> bool:       # type: ignore
        if not self.is_cell(other_cell) or other_cell is None:
            return False
        return self.row == other_cell.row and self.column == other_cell.column
    
    def is_cell(self, cell: Any) -> bool:
        return isinstance(cell, Cell)
    
    def __iadd__(self, cell: "Cell") -> "Cell":
        """
        Overload for the += operator with the link method
        """
        self.link(cell)
        return self
    
    def __hash__(self):
        return hash((self.row, self.column))