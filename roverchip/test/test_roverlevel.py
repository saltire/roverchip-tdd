import unittest

from roverchip.roverlevel import RoverLevel

from test_level import MockDataFile


class Test_RoverLevel(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0],
                 [0, 0, 1]]
        ctypes = [('Floor',), ('Exit',)]
        self.level = RoverLevel(*MockDataFile(cells, ctypes).get_data())

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
