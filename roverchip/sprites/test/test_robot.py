import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Robot(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
        ctypes = [('Floor',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.robot = self.level.add_sprite('Robot', (1, 1))

        self.celltime = 1000 / self.robot.speed


    def test_robot_rotates_left_if_follow_dir_is_zero(self):
        self.robot.start_turn()
        self.assertEqual(self.robot.rotate, 3)


    def test_robot_rotates_right_if_follow_dir_is_one(self):
        self.robot.follow_dir = 1
        self.robot.start_turn()
        self.assertEqual(self.robot.rotate, 1)


    def test_robot_move_dir_matches_rotate_dir(self):
        self.robot.start_turn()
        self.assertEqual(self.robot.move_dir, 3)


    def test_robot_moves_if_unobstructed(self):
        self.robot.start_turn()
        self.assertEqual(self.robot.to_move, 1)


    def test_robot_moves_straight_if_edge_in_follow_dir(self):
        self.robot.pos = (0, 1)
        self.robot.start_turn()
        self.assertEqual(self.robot.move_dir, 0)


    def test_robot_moves_straight_if_object_in_follow_dir(self):
        self.level.add_sprite('Crate', (0, 1))
        self.robot.start_turn()
        self.assertEqual(self.robot.move_dir, 0)


    def test_robot_rotates_opposite_way_if_obstructed_in_follow_dir_and_ahead(self):
        self.level.add_sprite('Crate', (0, 1))
        self.level.add_sprite('Crate', (1, 0))
        self.robot.start_turn()
        self.assertEqual(self.robot.move_dir, 1)


    def test_robot_does_180_if_obstructed_ahead_and_on_both_sides(self):
        self.robot.pos = (0, 0)
        self.level.add_sprite('Crate', (1, 0))
        self.robot.start_turn()
        self.assertEqual(self.robot.move_dir, 2)


    def test_robot_kills_player_on_entering_players_cell(self):
        player = self.level.add_sprite('Player', (0, 1))
        self.level.update_level([], 1)
        self.assertNotIn(player, self.level.sprites)
