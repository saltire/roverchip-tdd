import pygame

import config
from renderer import Renderer
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
        self.renderer = Renderer(self.tileset)
        
        self.redraw = True
        
        
    def resize_view(self):
        """Given the window size, set view size and cell size,
        then resize the view and tileset."""
        windowsize = self.window_view.get_size()
        vw, vh = config.maxviewcells
        
        # set view size in cells and cell size in pixels
        self.viewcells = min(vw, self.level.width), min(vh, self.level.height)
        self.cellsize = self.get_cell_size(windowsize, self.viewcells)
        
        # resize view and tileset, and schedule a full redraw
        self.view = self.window_view.subsurface(
                        self.get_view_rect(windowsize, self.viewcells))
        self.tileset.resize_tileset(self.cellsize)
        self.redraw = True
        
        
    def get_cell_size(self, (ww, wh), (vw, vh)):
        """Given a window size in pixels, and a view size in cells,
        return the largest cell size that will fit the view in the window."""
        return min(ww / vw, wh / vh)
    
    
    def get_view_rect(self, (ww, wh), (vw, vh)):
        """Given the cell size, return the offset and size of the view."""
        width, height = vw * self.cellsize, vh * self.cellsize
        left, top = int((ww - width) / 2), int((wh - height) / 2)
        return left, top, width, height


    def draw_frame(self):
        if self.redraw:
            # draw the background
            self.background = pygame.Surface(
                (self.level.width * self.cellsize,
                 self.level.height * self.cellsize))
            for (cx, cy), cell in self.level.cells.items():
                self.background.blit(self.renderer.render(cell),
                                     (cx * self.cellsize, cy * self.cellsize))
                
            self.redraw = False
        
        # find offset that places the player in the centre
        px, py = self.level.sprites_by_type('Player')[0].pos
        vw, vh = self.viewcells
        ox = px - (vw - 1) / 2.0
        oy = py - (vh - 1) / 2.0
        
        # clamp values so as not to go off the edge
        ox = max(0, min(ox, self.level.width - vw))
        oy = max(0, min(oy, self.level.height - vh))

        # blit background onto the view
        left, top = int(ox * self.cellsize), int(oy * self.cellsize)
        width, height = self.view.get_size()
        self.view.blit(self.background, (0, 0), (left, top, width, height))
        
        # blit sprites onto the view
        for sprite in self.level.sprites:
            sx, sy = sprite.pos
            self.view.blit(self.renderer.render(sprite),
                (sx * self.cellsize - left, sy * self.cellsize - top))
    
    
    def run_frame(self, elapsed, keys):
        # handle events
        events = []
        for key, keydown in keys:
            # skip level
            if keydown and key == pygame.K_RETURN:
                return True
            
            # move event
            if key in self.move_keys:
                events.append(('move', self.move_keys.index(key), keydown))
        
        self.level.update_level(events, elapsed)
        
        if self.level.check_for_failure():
            return False
        if self.level.check_for_success():
            return True
        
        