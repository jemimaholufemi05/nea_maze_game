from core.cell import Cell
""" 
Test that multiple references to the same location are equivalent i.e.
Different instances of a the same location are the same i.e. Cell(1,1)
No matter how many times it is created still refers to the same location
in the grid
"""
def test_equality():
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 1)
    assert a_cell == another_cell
"""
Cells are not linked by default, to link cell that
are next to each other they have to be explicitly linked
using the link operation
"""
def test_linking():
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)
    # the above cells are not linked
    assert a_cell.is_linked(another_cell) is False
    assert another_cell.is_linked(a_cell) is False
    assert a_cell.is_linked(yet_another_cell) is False
    assert another_cell.is_linked(yet_another_cell) is False
    # the operation below link a_cell to another_cell
    a_cell.link(another_cell)
    # now we can test the linkage
    assert a_cell.is_linked(another_cell) is True
    assert another_cell.is_linked(a_cell) is True
    assert a_cell.is_linked(yet_another_cell) is False
    assert another_cell.is_linked(yet_another_cell) is False
"""
This test how to unlink cells
"""
def test_unlinking() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)
    a_cell.link(another_cell)
    a_cell.link(yet_another_cell)
    assert a_cell.is_linked(another_cell) is True
    assert another_cell.is_linked(a_cell) is True
    assert a_cell.is_linked(yet_another_cell) is True
    a_cell.unlink(another_cell)
    assert a_cell.is_linked(another_cell) is False
    assert another_cell.is_linked(a_cell) is False
    assert a_cell.is_linked(yet_another_cell) is True
    assert yet_another_cell.is_linked(a_cell) is True
"""
 Test that a single Cell instance has no neighbouring cells
"""
def test_has_no_neighbors() -> None:
    assert Cell(1, 1).neighbours == []
"""
Test to show neighbours around each other
"""  
def test_has_neighbors() -> None:
    a_cell = Cell(1, 1)
    another_cell = Cell(1, 2)
    yet_another_cell = Cell(2, 1)
    a_cell.north = another_cell
    another_cell.south = yet_another_cell
    yet_another_cell.east = another_cell
    yet_another_cell.west = a_cell
    assert another_cell in a_cell.neighbours
    assert yet_another_cell not in a_cell.neighbours
    assert len(a_cell.neighbours) == 1
    assert a_cell not in another_cell.neighbours
    assert yet_another_cell in another_cell.neighbours
    assert len(another_cell.neighbours) == 1
    assert a_cell in yet_another_cell.neighbours
    assert another_cell in yet_another_cell.neighbours
    assert len(yet_another_cell.neighbours) == 2
def test_distances() -> None:
    a_cell = Cell(0, 0)
    another_cell = Cell(0, 1)
    yet_another_cell = Cell(0, 2)
    a_cell.east = another_cell
    a_cell += another_cell
    another_cell.east = yet_another_cell
    another_cell += yet_another_cell
    distances = a_cell.distances
    assert set(distances.cells) == {yet_another_cell, another_cell, a_cell}
    assert distances[a_cell] == 0
    assert distances[another_cell] == 1
    assert distances[yet_another_cell] == 2