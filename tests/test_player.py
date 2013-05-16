import unittest

from test_level import MockLevel


class Test_Player(unittest.TestCase):
    def setUp(self):
        celldata = [[1, 1, 1],
                    [0, 0, 0],
                    [0, 0, 0]]
        ctypes = [('Floor',),
                  ('Wall',)]
        
        self.level = MockLevel(celldata, ctypes)
        
        self.player = self.level.add_sprite('Player', (0, 1))
        self.crate = self.level.add_sprite('Crate', (1, 1))
        
        self.celltime = 1000 / self.player.speed # time to move 1 cell
        
        
    def test_player_enters_cells_with_movables(self):
        self.player.start_move(1)
        self.assertEqual(self.player.to_move, 1)
        
        
    def test_player_pushes_movable_objects(self):
        self.player.start_move(1)
        self.assertItemsEqual(self.player.pushing, [self.crate])
        
        
    def test_player_moves_pushed_objects(self):
        self.player.start_move(1)
        self.player.do_move(self.celltime)
        self.assertEqual(self.crate.pos, (2, 1))
        
        
    def test_player_doesnt_push_movable_without_empty_cell_behind(self):
        self.level.add_sprite('Crate', (2, 1))
        self.player.start_move(1)
        self.assertEqual(self.player.to_move, 0)
        