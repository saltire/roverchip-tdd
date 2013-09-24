import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Rover(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0]]
        ctypes = [('Floor',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (0, 0))
        self.rover = self.level.add_sprite('Rover', (2, 0))

        self.celltime = 1000 / self.player.speed  # time to move 1 cell


    def test_rover_follows_player_after_player_moves_adjacent(self):
        self.player.start_move(1)
        self.level.update_level([], self.celltime)
        self.assertIn(self.rover, self.player.followers)


    def test_rover_faces_toward_players_last_position(self):
        self.player.pos = 1, 0
        self.player.followers.add(self.rover)
        self.player.start_move(3)
        self.level.update_level([], self.celltime)
        self.assertEqual(self.rover.rotate, 3)
