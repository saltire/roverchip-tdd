import unittest

from roverchip.level import Level


class MockLevel(Level):
    def __init__(self, cells, ctypes, spritedata):
        celldata = {}
        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                celldata[x, y] = ctypes[cell][0]
        
        Level.__init__(self, celldata, spritedata)


class Test_Level(unittest.TestCase):
    def setUp(self):
        cells = [[1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]
                 ]
        ctypes = [('Floor',),
                  ('Grate',)
                  ]
        spritedata = [('Player', (1, 2)),
                      ('Crate', (1, 1)),
                      ]
        self.level = MockLevel(cells, ctypes, spritedata)
        
        
    def test_level_has_correct_cell_types(self):
        for (x, y), celltype in [((0, 0), 'Grate'),
                                 ((1, 1), 'Floor')
                                 ]:
            self.assertEqual(self.level.cells[x, y].get_type(), celltype)
    
    
    def test_level_has_correct_sprite_types(self):
        classes = [sprite.get_type() for sprite in self.level.sprites]
        self.assertItemsEqual(classes, ['Player', 'Crate'])
        
    
    def test_sprites_cant_enter_cells_out_of_bounds(self):
        self.assertTrue(self.level.sprite_can_enter((0, 0)))
        self.assertTrue(self.level.sprite_can_enter((3, 2)))
        self.assertFalse(self.level.sprite_can_enter((0, 3)))
        self.assertFalse(self.level.sprite_can_enter((-1, -1)))
        