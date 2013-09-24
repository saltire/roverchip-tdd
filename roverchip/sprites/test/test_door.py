import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class TestDoor(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0]]
        ctypes = [('Floor',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (0, 0))
        self.door = self.level.add_sprite('Door', (1, 0), 3)


    def test_door_opens_when_player_walks_through_with_key(self):
        self.player.carrying.add(self.level.add_sprite('Key', (0, 0)))
        self.player.attempt_move(1)
        self.assertFalse(self.door.is_solid)
