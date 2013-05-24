import unittest

from pyg.cellrenderer import CellRenderer


class MockTileset:
    def get_tile(self, (x, y)):
        return x, y
    

    
class NormalCell:
    def get_type(self):
        return self.__class__.__name__
    


class SpecialCell(NormalCell):
    def __init__(self):
        self.offset = 2
    

    
class MockCellRenderer(CellRenderer):
    def __init__(self, tileset):
        CellRenderer.__init__(self, tileset)
        
        self.tiles['NormalCell'] = (0, 0)
        
        
    def render_specialcell(self, cell):
        return self.tileset.get_tile((1 + cell.offset, 1 + cell.offset))
        


class Test_CellRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = MockCellRenderer(MockTileset())
        
    
    def test_normal_cell_type_returns_correct_tile(self):
        self.assertEqual(self.renderer.render_cell(NormalCell()), (0, 0))
        
        
    def test_special_cell_type_returns_correctly_modified_tile(self):
        self.assertEqual(self.renderer.render_cell(SpecialCell()), (3, 3))
        