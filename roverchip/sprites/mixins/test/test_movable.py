import unittest

from roverchip.level import Level
from roverchip.sprite import Sprite
from roverchip.sprites.mixins.movable import Movable

from roverchip.test.test_level import MockDataFile


class MockMovable(Movable, Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))


class Test_Movable(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 1, 0]]
        ctypes = [('Floor',), ('Fire',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (0, 0))
        self.movable = MockMovable(self.level, (1, 0))
        self.level.sprites.add(self.movable)

        self.celltime = 1000 / self.player.speed  # time to move 1 cell


    def test_movable_item_has_movable_attribute(self):
        self.assertTrue(self.movable.is_movable)


    def test_movable_item_moves_over_fire(self):
        self.player.attempt_move(1)
        self.level.update_level([], self.celltime * 2)
        self.assertEqual(self.movable.pos, (3, 0))


    def test_movable_item_doesnt_move_over_fire_if_blocked(self):
        self.level.add_sprite('Crate', (3, 0))
        self.player.attempt_move(1)
        self.level.update_level([], self.celltime * 2)
        self.assertEqual(self.movable.pos, (2, 0))
