import unittest

from roverchip.game import Game
from roverchip.levels.level import Level

from roverchip.levels.test.test_level import MockDataFile


class MockLevelWithConditions(Level):
    def check_for_success(self):
        return self.sprites_by_type('Player')[0].pos == (2, 1)
    
    
    def check_for_failure(self):
        return self.sprites_by_type('Player')[0].pos == (0, 1)
    
    

class MockEventHandler:
    def __init__(self):
        self.events = []
        
        
    def get_events(self):
        events = self.events
        self.events = []
        return events
    
    
    def add_event(self, etype, *args):
        self.events.append((etype, args))
        
        
        
class Renderer:
    def render_level(self, level):
        pass
    
    

class MockGame(Game):
    def __init__(self, eventhandler, renderer, leveldata):
        self.eventhandler = eventhandler
        self.renderer = renderer
        
        self.level = MockLevelWithConditions(*MockDataFile(*leveldata).get_data())
    


class Test_Game(unittest.TestCase):
    def setUp(self):
        cells = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
        ctypes = [('Floor',)]
        
        self.game = MockGame(MockEventHandler(), Renderer(), (cells, ctypes))
        self.player = self.game.level.add_sprite('Player', (1, 1))
        
        
    def test_game_frame_returns_none_if_no_success_or_failure(self):
        self.assertIsNone(self.game.run_frame(0, []))
    
    
    def test_game_frame_returns_true_on_success(self):
        self.player.pos = 2, 1
        self.assertIs(self.game.run_frame(0, []), True)
        

    def test_game_frame_returns_false_on_failure(self):
        self.player.pos = 0, 1
        self.assertIs(self.game.run_frame(0, []), False)
        
        
    def test_move_event_starts_player_moving(self):
        self.game.run_frame(0, [('move', 2)])
        self.assertEqual(self.player.to_move, 1)
        
        
    def test_move_event_starts_player_moving_in_correct_direction(self):
        self.game.run_frame(0, [('move', 2)])
        self.assertEqual(self.player.move_dir, 2)
        
    
    
        