import pygame

import config
from screen import Screen
from tileset import Tileset
#from roverchip.game import Game
from roverchip.levels import leveltypes


class GameScreen(Screen):
    move_keys = pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT
    
    def __init__(self, leveldata):
        #self.game = Game(self, self, leveldata)
        self.level = leveltypes[leveldata.leveltype](*leveldata.get_data())
        self.tileset = Tileset(config.tilepath, config.tilesize)
        
        
    def resize_view(self, windowsize):
        """Given the window size, set cell size, and resize the view
        and the tileset."""
        # find the largest rectangle with the same ratio as viewcells
        ww, wh = windowsize
        vw, vh = config.viewcells
        self.cellsize = min(ww / vw, wh / vh)
        
        width, height = vw * self.cellsize, vh * self.cellsize
        left, top = int((ww - width) / 2), int((wh - height) / 2)
        self.view = self.window_view.subsurface((left, top, width, height))
        
        self.tileset.init_tileset(self.cellsize)


    def draw_frame(self):
        if not hasattr(self, 'background'):
            # draw the background
            self.background = pygame.Surface((self.level.width * self.cellsize,
                                              self.level.height * self.cellsize))

        # find offset that places the player in the centre
        px, py = self.level.sprites_by_type('Player')[0].pos
        vw, vh = config.viewcells
        ox = px - (vw - 1) / 2.0
        oy = py - (vh - 1) / 2.0
        
        # clamp values so as not to go off the edge
        ox = max(0, min(ox, self.level.width - vw))
        oy = max(0, min(oy, self.level.height - vh))

        # blit background onto the view
        left, top = int(ox * self.cellsize), int(oy * self.cellsize)
        width, height = self.view.get_size()
        self.view.blit(self.background, (0, 0), (left, top, width, height))
            
    
    
    def run_frame(self, elapsed, keys):
        # handle move events
        for key, keydown in keys:
            if key in self.move_keys and keydown:
                self.level.handle_event('move', self.move_keys.index(key))
        
        self.level.update_level(elapsed)
        
        