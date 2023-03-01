from core.cell import Cell
# from core.cell_3d import Cell3D
def test_equality():
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 1)
    
  #  a_cell3d = Cell3D (1, 1, 1)
   # another_cell3d = Cell3D (1, 1, 1)
    
    assert a_cell == another_cell  
   # assert a_cell3d == another_cell3d
def test_linking():
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    
    assert a_cell.is_linked(another_cell) is False 
    assert another_cell.is_linked(a_cell) is False
    
    a_cell.link(another_cell) 
    
    assert a_cell.is_linked(another_cell) is True 
    assert another_cell.is_linked(a_cell) is True
    
def test_unlinking():
    pass
def test_has_no_neighbours():
    pass
def test_has_neighbours():
    pass
