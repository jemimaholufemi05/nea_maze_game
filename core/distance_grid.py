from typing import Optional
from core.cell import Cell

from core.distances import Distances
from core.grid import Grid


class DistanceGrid(Grid):

    def __init__(self, rows: int, columns: int) -> None:
        super().__init__(rows, columns)
        self._distances: Optional[Distances] = None
        self.maximum: int = 0

    @property
    def distances(self) -> Optional[Distances]:
        return self._distances

    @distances.setter
    def distances(self, value: Optional[Distances]) -> None:
        self._distances = value
        if self._distances:
            _, self.maximum = self._distances.max

    def contents_of(self, cell: Cell) -> str:
        if self.distances is not None and self.distances[cell] is not None:
            return format(self.distances[cell], "1X").center(3)
        else:
            return super().contents_of(cell)