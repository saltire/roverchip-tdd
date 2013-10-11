import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Toggle(unittest.TestCase):
    def setUp(self):
        cells = [[0, 1, 0]]
        ctypes = [('Floor',), ('ToggleButton',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.toggle = self.level.add_sprite('Toggle', (2, 0), True)


    def test_player_stepping_on_button_reverses_toggle(self):
        self.assertTrue(self.toggle.is_solid)

        player = self.level.add_sprite('Player', (0, 0))
        player.attempt_move(1)
        self.level.update_level([], 1000 / player.speed)
        self.assertFalse(self.toggle.is_solid)
