import unittest

from test_level import MockLevel


class Test_Sprite(unittest.TestCase):
    def setUp(self):
        cells = [[1, 0, 0],
                 [1, 0, 0],
                 [1, 0, 0]]
        ctypes = [('Floor',), ('Wall',)]
        
        self.level = MockLevel(cells, ctypes)
        
        self.sprite = self.level.add_sprite('Sprite', (1, 2))
        
        self.celltime = 1000 / self.sprite.speed # time to move 1 cell
    
    
    def test_sprite_has_correct_pos(self):
        self.assertEqual(self.sprite.pos, (1, 2))
        
        
    def test_sprite_saves_movement(self):
        self.sprite.start_move(1)
        self.assertEqual(self.sprite.to_move, (1, 1))
        

    def test_sprite_subtracts_movement(self):
        self.sprite.to_move = 1, 1
        self.sprite.do_move(self.celltime / 2)
        self.assertEqual(self.sprite.to_move, (0.5, 1))
        

    def test_sprite_moves_correct_distance(self):
        self.sprite.to_move = 1, 1
        self.sprite.do_move(self.celltime / 2)
        self.assertEqual(self.sprite.pos, (1.5, 2))
        
    
    def test_sprite_moves_up_to_remaining(self):
        self.sprite.to_move = 0.5, 1
        self.sprite.do_move(self.celltime)
        self.assertEqual(self.sprite.pos, (1.5, 2))


    def test_sprite_doesnt_move_outside_boundaries(self):
        self.sprite.start_move(2)
        self.assertEqual(self.sprite.to_move[0], 0)


    def test_sprite_doesnt_enter_solid_cell(self):
        self.sprite.start_move(3)
        self.assertEqual(self.sprite.to_move[0], 0)


    def test_sprite_doesnt_enter_cells_with_solid_sprites(self):
        self.level.add_sprite('Crate', (2, 2))
        self.sprite.start_move(1)
        self.assertEqual(self.sprite.to_move[0], 0)
        
        