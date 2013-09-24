import unittest

from roverchip.levels.rescuerover import RescueRover

from roverchip.test.test_level import MockDataFile


class Test_RescueRover(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0],
                 [0, 0, 1]]
        ctypes = [('Floor',), ('Exit',)]
        self.level = RescueRover(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (2, 0))
        self.rover = self.level.add_sprite('Rover', (0, 0))


    def test_level_doesnt_succeed_if_rover_not_following(self):
        self.player.pos = 2, 1
        self.assertFalse(self.level.check_for_success())


    def test_level_doesnt_succeed_if_player_not_on_exit(self):
        self.player.followers.add(self.rover)
        self.assertFalse(self.level.check_for_success())


    def test_level_succeeds_if_rover_following_and_player_on_exit(self):
        self.player.pos = 2, 1
        self.player.followers.add(self.rover)
        self.assertTrue(self.level.check_for_success())


    def test_level_fails_if_player_not_active(self):
        self.assertFalse(self.level.check_for_failure())
        self.player.is_active = False
        self.assertTrue(self.level.check_for_failure())
