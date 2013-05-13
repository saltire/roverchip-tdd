import unittest

from test_level import MockLevel


class Test_Sprite(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
        ctypes = [('Floor',)]
        spritedata = [('Sprite', (1, 2))]
        self.level = MockLevel(cells, ctypes, spritedata)
        
        self.sprite = self.level.sprites[0]
    
    
    def test_sprite_has_correct_pos(self):
        self.assertEqual(self.sprite.pos, (1, 2))
        
        
    def test_sprite_saves_movement(self):
        self.sprite.start_move(1) # east
        self.assertEqual(self.sprite.to_move, (1, 1))
        

    def test_sprite_subtracts_movement(self):
        self.sprite.to_move = 1, 1
        self.sprite.do_move(125) # call movement hook with elapsed ms
        self.assertEqual(self.sprite.to_move, (0.5, 1))
        

    def test_sprite_moves_correct_distance(self):
        self.sprite.to_move = 1, 1
        self.sprite.do_move(125)
        self.assertEqual(self.sprite.pos, (1.5, 2))
        
    
    def test_sprite_moves_up_to_remaining(self):
        self.sprite.to_move = 0.5, 1
        self.sprite.do_move(1000)
        self.assertEqual(self.sprite.pos, (1.5, 2))


    def test_sprite_cant_move_outside_boundaries(self):
        self.sprite.start_move(2)
        self.assertEqual(self.sprite.to_move[0], 0)
        