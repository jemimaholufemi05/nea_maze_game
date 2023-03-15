from core.cell import Cell 

class Cell3D(Cell):
    @property
    def up(self):
        return self._up
    @up.setter
    def up(self, up):
        self._up = up
    
    @property
    def down(self):
        return self._down 
    @down.setter
    def down(self, down):
        self._down = down
        
    @property
    def level(self):
        return self._level
    @level.setter
    def level(self, level):
        self._level = level
        
    def __init__(self, row: int, column: int, level: int):
        super().__init__(row, column)
        self._level = level
        self._up = None
        self._down = None
    
    def neighbours(self):
        list = super().neighbours()
        self.up and list.append(self.up)
        self.down and list.append(self.down)
        return list
              