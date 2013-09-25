import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Door(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0]]
        ctypes = [('Floor',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (0, 0))
        self.door = self.level.add_sprite('Door', (1, 0))
        self.key = self.level.add_sprite('Key', (0, 0))
        self.player.carrying.add(self.key)


    def test_door_opens_when_player_walks_through_with_key(self):
        self.player.attempt_move(1)
        self.assertFalse(self.door.is_solid)


    def test_key_disappears_after_use(self):
        self.player.attempt_move(1)
        self.assertFalse(self.key.is_active)


    def test_doors_use_only_one_key_if_multiple_carried(self):
        key2 = self.level.add_sprite('Key', (0, 0))
        self.player.carrying.add(key2)
        self.player.attempt_move(1)
        self.assertEqual(len(self.player.carrying), 1)


    def test_doors_use_correct_key_if_multiple_colours_carried(self):
        key2 = self.level.add_sprite('Key', (0, 0), 1)
        self.player.carrying.add(key2)
        self.player.attempt_move(1)
        self.assertItemsEqual(self.player.carrying, [key2])


    def test_door_doesnt_open_and_key_doesnt_disappear_if_colours_dont_match(self):
        self.key.colour = 1
        self.player.attempt_move(1)
        self.assertTrue(self.door.is_solid)
        self.assertTrue(self.key.is_active)
