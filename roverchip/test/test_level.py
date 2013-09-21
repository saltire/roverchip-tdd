import unittest

from roverchip.leveldata.leveldata import LevelData
from roverchip.level import Level


class MockDataFile(LevelData):
    def __init__(self, cells, ctypes, sprites=[], leveltype='Level'):
        self.leveltype = leveltype

        self.celldata = {}
        for y, row in enumerate(cells):
            for x, cell in enumerate(row):
                self.celldata[x, y] = ctypes[cell]

        self.spritedata = sprites


    def get_data(self):
        return self.celldata, self.spritedata


class Test_Level(unittest.TestCase):
    def setUp(self):
        cells = [[1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]
                 ]
        ctypes = [('Floor',),
                  ('Grate',)
                  ]
        self.level = Level(*MockDataFile(cells, ctypes).get_data())

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


    def test_level_returns_sprites_at_cell(self):
        self.assertItemsEqual(self.level.sprites.at((1, 2)), [self.player])
        self.assertItemsEqual(self.level.sprites.at((1, 1)), [self.crate])
        self.assertItemsEqual(self.level.sprites.at((1, 0)), [])


    def test_level_returns_sprites_partially_in_cell(self):
        crate = self.level.add_sprite('Crate', (2.5, 2))
        self.assertItemsEqual(self.level.sprites.on((2, 1)), [])
        self.assertItemsEqual(self.level.sprites.on((2, 2)), [crate])
        self.assertItemsEqual(self.level.sprites.on((3, 2)), [crate])


    def test_level_returns_sprites_by_type(self):
        self.assertItemsEqual(self.level.sprites['Player'], [self.player])
        self.assertItemsEqual(self.level.sprites['Crate'], [self.crate])
        self.assertItemsEqual(self.level.sprites['Random'], [])


    def test_sprites_cant_enter_cells_out_of_bounds(self):
        self.assertTrue(self.level.sprite_can_enter((0, 0)))
        self.assertTrue(self.level.sprite_can_enter((3, 2)))
        self.assertFalse(self.level.sprite_can_enter((0, 3)))
        self.assertFalse(self.level.sprite_can_enter((-1, -1)))


    def test_sprites_cant_enter_cells_with_movables(self):
        self.assertFalse(self.level.sprite_can_enter((1, 1)))


    def test_robots_cant_enter_no_robot_cells_even_If_empty(self):
        self.assertFalse(self.level.robot_can_enter((1, 0)))


    def test_player_can_enter_cells_with_movables(self):
        self.assertTrue(self.level.player_can_enter((1, 1)))
