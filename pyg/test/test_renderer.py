import unittest

from pyg.renderer import Renderer


class MockTileset:
    def get_tile(self, (x, y), rotate=0):
        return x, y, rotate


class NormalCell:
    def __init__(self):
        self.rotate = 1


    def get_type(self):
        return self.__class__.__name__


class SpecialCell(NormalCell):
    def __init__(self):
        self.rotate = 1
        self.offset = 2


class MockRenderer(Renderer):
    def __init__(self, tileset):
        Renderer.__init__(self, tileset)

        self.tiles['NormalCell'] = (0, 0)


    def render_specialcell(self, cell):
        return self.tileset.get_tile((1 + cell.offset, 1 + cell.offset),
                                     cell.rotate)


class Test_CellRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = MockRenderer(MockTileset())


    def test_normal_cell_type_returns_correct_tile(self):
        self.assertEqual(self.renderer.render(NormalCell()), (0, 0, 1))


    def test_special_cell_type_returns_correctly_modified_tile(self):
        self.assertEqual(self.renderer.render(SpecialCell()), (3, 3, 1))
