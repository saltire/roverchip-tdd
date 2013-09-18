import sys

import pygame

import config


class Window:
    def __init__(self, size=config.windowsize):
        pygame.init()

        # init a joystick if connected
        if pygame.joystick.get_count():
            pygame.joystick.Joystick(0).init()

        self.clock = pygame.time.Clock()

        self.screens = []
        self.init_window(size)


    def init_window(self, size, screen=None):
        """Initialize the game window. Called at beginning, and every time
        the window is resized."""
        # enforce minimum size
        (mw, mh), (w, h) = config.minsize, size
        if w < mw or h < mh:
            size = mw, mh

        # init view surface and pass it to screen
        self.view = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.view.fill((0, 0, 0))
        if screen is not None:
            screen.resize_view()


    def run(self, screen):
        """Run the loop for this screen."""
        self.screens.append(screen)
        screen.set_window(self)

        result = None

        while True:
            # update display
            screen.draw_frame()
            pygame.display.update()

            # break loop if screen returns a result
            if result is not None:
                # return to the previous screen (or exit)
                self.screens.pop()
                return result

            # tick clock
            elapsed = float(self.clock.tick(60))

            # get events, pass input events to level
            events = []
            for event in pygame.event.get():
                # close window
                if event.type == pygame.QUIT:
                    sys.exit()

                # resize window
                elif event.type == pygame.VIDEORESIZE:
                    self.init_window(event.size, screen)

                elif event.type in (pygame.KEYDOWN, pygame.KEYUP,
                                    pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN):
                    events.append(event)

            # run a frame of this screen
            result = screen.run_frame(elapsed, events)
