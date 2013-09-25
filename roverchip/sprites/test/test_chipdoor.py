import unittest

from roverchip.levels.chipschallenge import ChipsChallenge

from roverchip.test.test_level import MockDataFile


class Test_ChipDoor(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0]]
        ctypes = [('Floor',)]
        self.level = ChipsChallenge(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (0, 0))
        self.door = self.level.add_sprite('ChipDoor', (1, 0))
        self.player.carrying.add(self.level.add_sprite('Chip', (0, 0)))


    def test_door_opens_if_chip_quota_met(self):
        self.level.chipquota = 1
        self.player.attempt_move(1)
        self.assertFalse(self.door.is_solid)


    def test_door_doesnt_open_if_chip_quota_not_met(self):
        self.level.chipquota = 2
        self.player.attempt_move(1)
        self.assertTrue(self.door.is_solid)
