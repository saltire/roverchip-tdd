import unittest

import config
from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Sprite(unittest.TestCase):
    def setUp(self):
        cells = [[1, 0, 0],
                 [1, 0, 0],
                 [1, 0, 0]]
        ctypes = [('Floor',), ('Wall',)]
        levelfile = MockDataFile(cells, ctypes)

        config.animation = True
        self.level = Level(levelfile)
        self.sprite = self.level.add_sprite('Sprite', (1, 2))
        self.celltime = 1000 / self.sprite.speed  # time to move 1 cell

        config.animation = False
        self.level_noanim = Level(levelfile)
        self.sprite_noanim = self.level_noanim.add_sprite('Sprite', (1, 2))
        self.celltime_noanim = 1000 / self.sprite.speed  # time to move 1 cell


    def test_sprite_has_correct_pos(self):
        self.assertEqual(self.sprite.pos, (1, 2))


    def test_sprite_saves_move_distance(self):
        self.sprite.start_move(1)
        self.assertEqual(self.sprite.to_move, 1)


    def test_sprite_saves_move_dir(self):
        self.sprite.start_move(1)
        self.assertEqual(self.sprite.move_dir, 1)


    def test_sprite_subtracts_movement(self):
        self.sprite.start_move(1)
        self.sprite.do_move(self.celltime / 2)
        self.assertEqual(self.sprite.to_move, 0.5)


    def test_sprite_moves_correct_distance_and_direction(self):
        self.sprite.start_move(1)
        self.sprite.do_move(self.celltime / 2)
        self.assertEqual(self.sprite.pos, (1.5, 2))


    def test_sprite_moves_up_to_remaining(self):
        self.sprite.to_move = 0.5
        self.sprite.move_dir = 1
        self.sprite.do_move(self.celltime)
        self.assertEqual(self.sprite.pos, (1.5, 2))


    def test_rotating_sprite_rotates_when_moving(self):
        self.sprite.tile_rotates = True
        self.sprite.start_move(1)
        self.assertEqual(self.sprite.rotate, 1)


    def test_non_rotating_sprite_doesnt_rotate_when_moving(self):
        self.sprite.tile_rotates = False
        self.sprite.start_move(1)
        self.assertEqual(self.sprite.rotate, 0)


    def test_non_animated_sprite_moves_full_square_immediately(self):
        self.sprite_noanim.start_move(0)
        self.sprite_noanim.do_move(1)
        self.assertEqual(self.sprite_noanim.pos, (1, 1))


    def test_non_animated_sprite_waits_its_speed_before_moving(self):
        self.sprite_noanim.start_move(0)
        self.sprite_noanim.do_move(self.celltime / 2)
        self.sprite_noanim.start_move(0)
        self.sprite_noanim.do_move(self.celltime / 2)
        self.assertEqual(self.sprite_noanim.pos, (1, 1))


    def test_non_animated_sprite_moves_again_after_waiting(self):
        self.sprite_noanim.start_move(0)
        self.sprite_noanim.do_move(self.celltime / 2)
        self.sprite_noanim.start_move(0)
        self.sprite_noanim.do_move(self.celltime / 2 + 1)
        self.assertEqual(self.sprite_noanim.pos, (1, 0))


    def test_non_animated_sprite_moves_again_after_moving_and_waiting(self):
        self.sprite_noanim.start_move(0)
        self.sprite_noanim.do_move(1)
        self.sprite_noanim.do_move(self.celltime - 1)
        self.sprite_noanim.start_move(0)
        self.sprite_noanim.do_move(1)
        self.assertEqual(self.sprite_noanim.pos, (1, 0))
