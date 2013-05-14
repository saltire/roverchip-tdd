import unittest

from roverchip.level import Level
from roverchip.sprites import spritetypes


class MockLevel(Level):
    def __init__(self, cells, ctypes):
        celldata = {}
        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                celldata[x, y] = ctypes[cell][0]
        
        Level.__init__(self, celldata, [])
        
    
    def add_sprite(self, spritetype, (x, y)):
        spr = spritetypes[spritetype](self, (x, y))
        self.sprites.append(spr)
        return spr



class Test_Level(unittest.TestCase):
    def setUp(self):
        cells = [[1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]
                 ]
        ctypes = [('Floor',),
                  ('Grate',)
                  ]
        self.level = MockLevel(cells, ctypes)
        
        self.player = self.level.add_sprite('Player', (1, 2))
        self.crate = self.level.add_sprite('Crate', (1, 1))
        
        
    def test_level_has_correct_cell_types(self):
        for (x, y), celltype in [((0, 0), 'Grate'),
                                 ((1, 1), 'Floor')
                                 ]:
            self.assertEqual(self.level.cells[x, y].get_type(), celltype)
    
    
    def test_level_has_correct_sprite_types(self):
        classes = [sprite.get_type() for sprite in self.level.sprites]
        self.assertItemsEqual(classes, ['Player', 'Crate'])
        
        
    def test_level_returns_sprites_in_cell(self):
        self.assertItemsEqual(self.level.sprites_at((1, 2)), [self.player])
        self.assertItemsEqual(self.level.sprites_at((1, 1)), [self.crate])
        self.assertItemsEqual(self.level.sprites_at((1, 0)), [])
        
        
    def test_level_returns_movables_in_cell(self):
        self.assertItemsEqual(self.level.movables_at((1, 2)), [])
        self.assertItemsEqual(self.level.movables_at((1, 1)), [self.crate])
        self.assertItemsEqual(self.level.movables_at((1, 0)), [])        
        
    
    def test_level_returns_solids_in_cell(self):
        self.assertItemsEqual(self.level.solids_at((1, 2)), [])
        self.assertItemsEqual(self.level.solids_at((1, 1)), [self.crate])
        self.assertItemsEqual(self.level.solids_at((1, 0)), [])        
        
    
    def test_sprites_cant_enter_cells_out_of_bounds(self):
        self.assertTrue(self.level.sprite_can_enter((0, 0)))
        self.assertTrue(self.level.sprite_can_enter((3, 2)))
        self.assertFalse(self.level.sprite_can_enter((0, 3)))
        self.assertFalse(self.level.sprite_can_enter((-1, -1)))
        
        
    def test_sprites_cant_enter_cells_with_movables(self):
        self.assertFalse(self.level.sprite_can_enter((1, 1)))
        

    def test_player_can_enter_cells_with_movables(self):
        self.assertTrue(self.level.player_can_enter((1, 1)))
        
        