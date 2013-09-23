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
            # TODO: render all columns at init, and rerender only if font size or row count changes
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


    def run_frame(self, elapsed, events):
        """Scan for keystrokes and either switch menus or take actions."""

        for event in events:
            # arrow keypresses
            if event.type == pygame.KEYDOWN and event.key in self.movekeys:
                movedir = self.movekeys.index(event.key)
                self._move_marker(((0, 1), (1, 0), (0, -1), (-1, 0))[movedir])

            # joystick hat motion
            elif event.type == pygame.JOYHATMOTION and event.joy == 0 and event.value != (0, 0):
                self._move_marker(event.value)

            # enter key or joystick button (currently any button from 0-3)
            elif ((event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or
                  (event.type == pygame.JOYBUTTONDOWN and event.button <= 3)):
                func = self.options[self.selected][1]
                args = self.options[self.selected][2:]

                # run the selected option, exiting afterward if it returns false
                result = getattr(self, func)(*args)
                if result is False:
                    return False

                # reset menu
                self.resize_view()
                self.selected = 0

            # escape key
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False


    def _move_marker(self, (dx, dy)):
        """Move the menu marker up, down, left or right."""
        col = self.selected / self.rows
        totalcols = (len(self.options) + self.rows - 1) / self.rows
        old_selected = self.selected

        if dy:
            # move marker up or down
            self.selected = max(0, min(self.selected - dy, len(self.options) - 1))
        elif dx:
            # move marker left or right
            if 0 <= col + dx < totalcols:
                # move up to last item in the column if we're below it
                self.selected = min(self.selected + (self.rows * dx),
                                    len(self.options) - 1)

        if self.selected != old_selected:
            self.redraw = True


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
        """Run each level in sequence. If one returns false, repeat it.
        If passed a number, skip that many levels."""
        for ldata in self.leveldata[i:]:
            while True:
                status = self.window.run(GameScreen(ldata))
                if status == True: # success
                    break
                if status == 'quit':
                    return False
        return False
