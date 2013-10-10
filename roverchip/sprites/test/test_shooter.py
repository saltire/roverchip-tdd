import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Shooter(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0]]
        ctypes = [('Floor',), ('Wall',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (1, 0))
        self.level.add_sprite('Shooter', (0, 0), 1)


    def test_shooter_kills_player_in_front(self):
        self.level.update_level([], 1)
        self.assertFalse(self.player.is_active)


    def test_shooter_kills_rover_in_front(self):
        self.player.pos = (2, 0)
        rover = self.level.add_sprite('Rover', (1, 0))
        self.level.update_level([], 1)
        self.assertFalse(rover.is_active)


    def test_shooter_kills_player_farther_in_front(self):
        self.player.pos = (2, 0)
        self.level.update_level([], 1)
        self.assertFalse(self.player.is_active)


    def test_shooter_doesnt_kill_player_beside(self):
        self.player.pos = (0, 1)
        self.level.update_level([], 1)
        self.assertTrue(self.player.is_active)


    def test_shooter_doesnt_kill_player_behind_wall(self):
        self.player.pos = (4, 0)
        self.level.update_level([], 1)
        self.assertTrue(self.player.is_active)


    def test_shooter_doesnt_kill_player_behind_crate(self):
        self.player.pos = (2, 0)
        self.level.add_sprite('Crate', (1, 0))
        self.level.update_level([], 1)
        self.assertTrue(self.player.is_active)
