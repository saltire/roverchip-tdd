import unittest

from roverchip.level import Level

from roverchip.test.test_level import MockDataFile


class Test_Player(unittest.TestCase):
    def setUp(self):
        cells = [[1, 1, 1],
                 [0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
        ctypes = [('Floor',), ('Wall',)]
        self.level = Level(MockDataFile(cells, ctypes))

        self.player = self.level.add_sprite('Player', (0, 1))
        self.crate = self.level.add_sprite('Crate', (1, 1))

        self.celltime = 1000 / self.player.speed  # time to move 1 cell


    def test_player_enters_cells_with_movables(self):
        self.player.attempt_move(1)
        self.assertEqual(self.player.to_move, 1)


    def test_player_pushes_movable_objects(self):
        self.player.attempt_move(1)
        self.assertIn(self.crate, self.player.pushing)


    def test_player_moves_pushed_objects(self):
        self.level.update_level(self.celltime, [('move', 1)])
        self.assertEqual(self.crate.pos, (2, 1))


    def test_player_doesnt_push_movable_with_solid_in_cell_behind(self):
        self.level.add_sprite('Robot', (2, 1.5))
        self.player.attempt_move(1)
        self.assertEqual(self.player.to_move, 0)


    def test_player_doesnt_push_movable_with_level_edge_behind(self):
        self.level.add_sprite('Crate', (0, 0))
        self.player.attempt_move(0)
        self.assertEqual(self.player.to_move, 0)


    def test_player_doesnt_push_without_passable_cell_behind_on_key_event(self):
        self.level.add_sprite('Crate', (0, 0))
        self.level.update_level(self.celltime, [('move', 0)])
        self.assertEqual(self.player.pos, (0, 1))


    def test_followers_move_when_player_moves(self):
        self.player.followers.add(self.crate)
        self.player.attempt_move(2)
        self.assertEqual(self.crate.to_move, 1)


    def test_followers_move_toward_players_last_position(self):
        self.player.followers.add(self.crate)
        self.player.attempt_move(2)
        self.assertEqual(self.crate.move_dir, 3)


    def test_player_picks_up_items_when_arriving_in_their_cell(self):
        key = self.level.add_sprite('Key', (0, 2))
        self.player.attempt_move(2)
        self.level.update_level(self.celltime)
        self.assertIn(key, self.player.carrying)


    def test_carried_items_move_with_player(self):
        key = self.level.add_sprite('Key', (0, 1))
        self.player.carrying.add(key)
        self.player.attempt_move(2)
        self.level.update_level(self.celltime)
        self.assertEqual(key.pos, (0, 2))


    def test_player_starts_moving_after_move_event(self):
        self.player.handle_action('move', 2)
        self.player.start_turn()
        self.assertEqual(self.player.to_move, 1)


    def test_player_moves_after_move_event(self):
        self.level.update_level(self.celltime, [('move', 2)])
        self.assertEqual(self.player.pos, (0, 2))


    def test_player_keeps_moving_until_key_released(self):
        self.level.update_level(self.celltime, [('move', 2)])
        self.level.update_level(self.celltime)
        self.assertEqual(self.player.pos, (0, 3))


    def test_player_stops_moving_when_key_released(self):
        self.level.update_level(self.celltime, [('move', 2)])
        self.level.update_level(self.celltime)
        self.level.update_level(self.celltime, [('move', 2, False)])
        self.assertEqual(self.player.pos, (0, 3))


    def test_player_keeps_moving_in_1st_direction_when_2nd_key_pressed(self):
        self.level.update_level(self.celltime, [('move', 2)])
        self.level.update_level(self.celltime, [('move', 1)])
        self.assertEqual(self.player.pos, (0, 3))


    def test_player_starts_moving_in_2nd_direction_when_1st_key_released(self):
        self.level.update_level(self.celltime, [('move', 2)])
        self.level.update_level(self.celltime, [('move', 1)])
        self.level.update_level(self.celltime, [('move', 2, False)])
        self.assertEqual(self.player.pos, (1, 3))
