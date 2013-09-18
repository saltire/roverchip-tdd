import pygame

import config
from font import Font
from gamescreen import GameScreen
from screen import Screen


class MenuScreen(Screen):
    def __init__(self):
        self.font = Font(config.menufontpath, config.menufontsize)

        # init menu display
        self.selected = 0
        self.col_offset = 0


    def resize_view(self):
        """Resize the menu view, redraw the background, and reinit the font."""
        # find the largest rectangle with the configured menu ratio,
        # that fits within the configured menu margins.
        ww, wh = self.window.view.get_size()
        bw, bh = config.menuratio
        mx, my = config.menumargin
        mult = min(ww * (1 - mx * 2) / bw, wh * (1 - my * 2) / bh)
        width, height = bw * mult, bh * mult
        left, top = (ww - width) / 2, (wh - height) / 2
        self.menuview = self.window.view.subsurface((left, top, width, height))

        # create a text rectangle that fits within configured text margins
        tmx, tmy = config.textmargin
        tleft, ttop = tmx * width, tmy * height
        twidth, theight = width - tleft * 2, height - ttop * 2
        self.textarea = self.menuview.subsurface((tleft, ttop, twidth, theight))

        # find biggest font size that will fit the max number of rows
        # with the given rheight, without going under the min size
        for size in range(config.maxfontsize, config.minfontsize - 1, -config.sizestep):
            totalheight = int(size * config.lineheight) * (config.maxrows - 1) + size
            if totalheight <= self.textarea.get_height():
                rows = config.maxrows
                break
            # only if no size in range fits: start reducing number of rows
            if size == config.minfontsize:
                for rows in range(config.maxrows - 1, 0, -1):
                    totalheight = int(size * config.lineheight) * (rows - 1) + size
                    if totalheight <= self.textarea.get_height():
                        break
        self.cheight = size
        self.rows = rows
        self.rheight = int(size * config.lineheight)

        # draw marker
        msize = self.cheight / 2
        self.marker = pygame.Surface((msize, msize))
        self.marker.fill(config.menumarkercolor)

        self.redraw = True


    def draw_frame(self):
        """Draw the visible columns of options on the screen, and the marker."""
        if self.redraw:
            self.window.view.fill((0, 0, 0))
            self.menuview.fill(config.menubackcolor)

            columns = config.columns
            colwidth = self.textarea.get_width() / columns
            srow = self.selected % self.rows
            scol = self.selected / self.rows

            # adjust offset to within (columns) of col
            self.col_offset = min(scol, max(self.col_offset, scol - columns + 1))

            # render and blit each column of options that is showing
            for c, col in enumerate(range(self.col_offset, columns)):
                opts = self.options[self.rows * col:self.rows * (col + 1)]
                opttext = self.font.render('\n'.join(opt[0] for opt in opts),
                                           charheight=self.cheight, lineheight=self.rheight,
                                           tracking=1, color=config.menufontcolor)
                self.textarea.blit(opttext, (c * colwidth + self.cheight, 0))

            # blit marker
            mmargin = self.cheight / 4
            self.textarea.blit(self.marker, ((scol - self.col_offset) * colwidth + mmargin,
                                             srow * self.rheight + mmargin))

            self.redraw = False


    def run_frame(self, elapsed, keys):
        """Scan for keystrokes and either switch menus or take actions."""
        for key, keydown in keys:
            # arrow keys: change selection
            if keydown and key in (pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT):
                col = self.selected / self.rows
                totalcols = (len(self.options) + self.rows - 1) / self.rows
                old_selected = self.selected

                if key in (pygame.K_UP, pygame.K_DOWN):
                    # move marker up or down
                    mod = 1 if key == pygame.K_DOWN else -1
                    self.selected = max(0, min(self.selected + mod, len(self.options) - 1))

                elif key == pygame.K_LEFT and col > 0:
                    # move marker left
                    self.selected -= self.rows

                elif key == pygame.K_RIGHT and col < totalcols - 1:
                    # move marker right
                    self.selected = min(self.selected + self.rows, len(self.options) - 1)

                if self.selected != old_selected:
                    self.redraw = True

            # enter key: open selected screen or quit this menu
            elif keydown and key == pygame.K_RETURN:
                func = self.options[self.selected][1]
                args = self.options[self.selected][2:]

                # run the selected option, exiting afterward if it returns false
                result = getattr(self, func)(*args)
                if result is False:
                    return False

                # reset menu
                self.resize_view()
                self.selected = 0

            # escape key: quit menu
            elif keydown and key == pygame.K_ESCAPE:
                return False


class MainMenuScreen(MenuScreen):
    def __init__(self, leveldata):
        self.leveldata = leveldata
        self.options = [('Play Game', 'play'),
                        ('Quit Game', 'quit'),
                        ]
        MenuScreen.__init__(self)


    def play(self):
        """Open up a level menu with a list of all levels."""
        self.window.run(LevelMenuScreen(self.leveldata))


    def quit(self):
        """Quit this screen."""
        return False


class LevelMenuScreen(MenuScreen):
    def __init__(self, leveldata):
        self.leveldata = leveldata
        self.options = [(ldata.title, 'level', i) for i, ldata in enumerate(leveldata)]
        MenuScreen.__init__(self)


    def level(self, i):
        """Run each level in sequence, stopping if one returns false.
        If passed a number, skip that many levels."""
        for ldata in self.leveldata[i:]:
            if self.window.run(GameScreen(ldata)) is False:
                return False
        return False
