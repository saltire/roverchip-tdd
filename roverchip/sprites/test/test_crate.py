import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class TestCrate(unittest.TestCase):
    def setUp(self):
        cells = [[1, 1],
                 [1, 4]
                 ]
        ctypes = [('Water', 0), ('Water', 1), ('Water', 2), ('Water', 3), ('Floor',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.crate = self.level.add_sprite('Crate', (0, 0))


    def test_crate_moves_if_in_flowing_water_with_water_beyond(self):
        self.crate.start_turn()
        self.assertEqual(self.crate.to_move, 1)


    def test_crate_moves_in_flow_direction(self):
        self.crate.start_turn()
        self.assertEqual(self.crate.move_dir, 1)


    def test_crate_doesnt_move_if_non_water_cell_beyond(self):
        self.crate.pos = (0, 1)
        self.crate.start_turn()
        self.assertEqual(self.crate.to_move, 0)


    def test_crate_doesnt_move_if_level_edge_beyond(self):
        self.crate.pos = (1, 0)
        self.crate.start_turn()
        self.assertEqual(self.crate.to_move, 0)


    def test_player_can_enter_crate_cell_when_in_water(self):
        self.crate.start_turn()
        self.assertTrue(self.level.player_can_enter((0, 0)))
