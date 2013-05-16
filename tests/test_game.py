import unittest

from roverchip.game import Game

from test_level import MockLevel


class MockLevelWithConditions(MockLevel):
    def check_for_success(self):
        return self.sprites_by_type('Player')[0].pos == (2, 1)
    
    
    def check_for_failure(self):
        return self.sprites_by_type('Player')[0].pos == (0, 1)
    


class Test_Game(unittest.TestCase):
    def setUp(self):
        celldata = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]
        ctypes = [('Floor',)]
        
        self.game = Game()
        self.level = MockLevelWithConditions(celldata, ctypes)
        
        self.player = self.level.add_sprite('Player', (1, 1))
        
        
    def test_game_frame_returns_none_if_no_success_or_failure(self):
        self.assertIsNone(self.game.run_frame(self.level))
    
    
    def test_game_frame_returns_true_on_success(self):
        self.player.pos = 2, 1
        self.assertIs(self.game.run_frame(self.level), True)
        

    def test_game_frame_returns_false_on_failure(self):
        self.player.pos = 0, 1
        self.assertIs(self.game.run_frame(self.level), False)
        