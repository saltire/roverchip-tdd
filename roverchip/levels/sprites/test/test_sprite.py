import unittest

from roverchip.levels.level import Level

from roverchip.levels.test.test_level import MockDataFile


class Test_Sprite(unittest.TestCase):
    def setUp(self):
        cells = [[1, 0, 0],
                 [1, 0, 0],
                 [1, 0, 0]]
        ctypes = [('Floor',), ('Wall',)]
        
        self.level = Level(*MockDataFile(cells, ctypes).get_data())
        
        self.sprite = self.level.add_sprite('Sprite', (1, 2))
        
        self.celltime = 1000 / self.sprite.speed # time to move 1 cell
    
    
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
        

    def test_sprite_moves_correct_distance(self):
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
        
        