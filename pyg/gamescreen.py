import operator

import pygame

import config
from renderer import Renderer
from screen import Screen
from tileset import Tileset
from roverchip import leveltypes


class GameScreen(Screen):
    def __init__(self, leveldata):
        celldata, spritedata = leveldata.get_data()
        self.level = leveltypes[leveldata.leveltype](celldata, spritedata, config.animation)
        self.tileset = Tileset(config.tilepath, config.tilesize)
        self.renderer = Renderer(self.tileset)

        self.redraw = True


    def resize_view(self):
        """Given the window size, set view size and cell size,
        then resize the view and tileset."""
        ww, wh = self.window.view.get_size()
        vw, vh = config.maxviewcells

        # set view size in cells and cell size in pixels
        self.viewcells = min(vw, self.level.width), min(vh, self.level.height)
        self.cellsize = self._get_cell_size((ww, wh), self.viewcells)

        # resize view and tileset, and schedule a full redraw
        self.view = self.window.view.subsurface(self._get_view_rect((ww, wh), self.viewcells))
        self.tileset.resize_tileset(self.cellsize)
        self.redraw = True


    def _get_cell_size(self, (ww, wh), (vw, vh)):
        """Given a window size in pixels, and a view size in cells,
        return the largest cell size that will fit the view in the window."""
        return min(ww / vw, wh / vh)


    def _get_view_rect(self, (ww, wh), (vw, vh)):
        """Given the cell size, return the offset and size of the view."""
        width, height = vw * self.cellsize, vh * self.cellsize
        left, top = int((ww - width) / 2), int((wh - height) / 2)
        return left, top, width, height


    def draw_frame(self):
        if self.redraw:
            # draw the background
            self.window.view.fill((0, 0, 0))
            self.background = pygame.Surface(
                (self.level.width * self.cellsize,
                 self.level.height * self.cellsize))
            for (cx, cy), cell in self.level.cells.items():
                tile = self.renderer.render(cell)
                if tile:
                    self.background.blit(tile, (cx * self.cellsize, cy * self.cellsize))

            self.redraw = False

        # find offset that places the player in the centre
        px, py = self.level.sprites['Player'].pop().pos
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
        for sprite in sorted(self.level.sprites.active, key=operator.attrgetter('layer')):
            sx, sy = sprite.pos
            tile = self.renderer.render(sprite)
            if tile:
                self.view.blit(tile, (sx * self.cellsize - left, sy * self.cellsize - top))


    def run_frame(self, elapsed, events):
        actions = []

        # handle events
        for event in events:
            # enter: skip level
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True

            # escape: quit to menu
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            # arrow keypresses
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN) and event.key in self.movekeys:
                actions.append(('move', self.movekeys.index(event.key),
                                event.type == pygame.KEYDOWN))

        self.level.update_level(actions, elapsed)

        if self.level.check_for_failure():
            return False
        if self.level.check_for_success():
            return True
