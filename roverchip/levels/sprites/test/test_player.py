import unittest

from roverchip.levels.level import Level

from roverchip.levels.test.test_level import MockDataFile


class Test_Player(unittest.TestCase):
    def setUp(self):
        cells = [[1, 1, 1],
                 [0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
        ctypes = [('Floor',),
                  ('Wall',)]
        
        self.level = Level(*MockDataFile(cells, ctypes).get_data())
        
        self.player = self.level.add_sprite('Player', (0, 1))
        self.crate = self.level.add_sprite('Crate', (1, 1))
        
        self.celltime = 1000 / self.player.speed # time to move 1 cell
        
        
    def test_player_enters_cells_with_movables(self):
        self.player.attempt_move(1)
        self.assertEqual(self.player.to_move, 1)
        
        
    def test_player_pushes_movable_objects(self):
        self.player.attempt_move(1)
        self.assertItemsEqual(self.player.pushing, [self.crate])
        
        
    def test_player_moves_pushed_objects(self):
        self.player.attempt_move(1)
        self.player.do_move(self.celltime)
        self.assertEqual(self.crate.pos, (2, 1))
        
        
    def test_player_doesnt_push_movable_without_empty_cell_behind(self):
        self.level.add_sprite('Crate', (2, 1))
        self.player.attempt_move(1)
        self.assertEqual(self.player.to_move, 0)
        
        
    def test_player_starts_moving_after_move_event(self):
        self.level.handle_event('move', 2)
        self.assertEqual(self.player.to_move, 1)
        
        
    def test_player_moves_after_move_event(self):
        self.level.handle_event('move', 2)
        self.player.do_move(self.celltime)
        self.assertEqual(self.player.pos, (0, 2))
        
        
    def test_player_moves_again_after_second_move_event(self):
        self.level.handle_event('move', 2)
        self.player.do_move(self.celltime)
        self.level.handle_event('move', 2)
        self.player.do_move(self.celltime)
        self.assertEqual(self.player.pos, (0, 3))
        
