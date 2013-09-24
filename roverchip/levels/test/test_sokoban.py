import unittest

from roverchip.levels.sokoban import Sokoban

from roverchip.test.test_level import MockDataFile


class Test_Sokoban(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 1, 1]]
        ctypes = [('Floor',), ('Grate',)]
        self.level = Sokoban(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (1, 0))
        self.level.add_sprite('Crate', (2, 2))


    def test_level_doesnt_succeed_without_all_crates_on_grates(self):
        self.level.add_sprite('Crate', (1, 1))
        self.assertFalse(self.level.check_for_success())


    def test_level_doesnt_succeed_with_crate_partially_on_grate(self):
        self.level.add_sprite('Crate', (1, 1.5))
        self.assertFalse(self.level.check_for_success())


    def test_level_succeeds_with_all_crates_on_grates(self):
        self.level.add_sprite('Crate', (1, 2))
        self.assertTrue(self.level.check_for_success())
