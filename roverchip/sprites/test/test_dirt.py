import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Dirt(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 1]]
        ctypes = [('Floor',), ('Water',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.dirt = self.level.add_sprite('Dirt', (1, 0))
        self.player = self.level.add_sprite('Player', (0, 0))


    def test_dirt_becomes_bridge_when_in_water(self):
        self.assertFalse(self.dirt.is_bridge)
        self.dirt.pos = 2, 0
        self.level.update_level()
        self.assertTrue(self.dirt.is_bridge)


    def test_dirt_doesnt_become_bridge_when_bridge_already_in_water(self):
        self.level.add_sprite('Dirt', (2, 0))
        self.level.update_level()
        self.dirt.pos = 2, 0
        self.level.update_level()
        self.assertFalse(self.dirt.is_bridge)


    def test_dirt_no_longer_solid_once_player_has_walked_on_it(self):
        self.dirt.pos = 2, 0
        self.level.update_level()
        self.assertTrue(self.dirt.is_solid)
        self.player.pos = 2, 0
        self.level.update_level()
        self.assertFalse(self.dirt.is_solid)
