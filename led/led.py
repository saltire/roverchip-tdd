import sys

import pygame

import config
from arduino import Arduino
from roverchip.levels import leveltypes


class LED:
    move_keys = pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT

    colours = {'Floor': (0, 0, 0),
               'Wall': (72, 72, 128),
               'Grate': (0, 128, 0),

               'Player': (255, 255, 0),
               'Crate': (255, 128, 0)
             }

    def __init__(self, (w, h)):
        self.arduino = Arduino('COM5', 9600)
        self.size = w, h

        pygame.init()
        self.clock = pygame.time.Clock()
        self.view = pygame.display.set_mode((w * 8, h * 8))


    def run_level(self, levelfile):
        config.animation = False
        level = leveltypes[levelfile.gametype](levelfile)

        w, h = self.size
        ox, oy = (w - level.width) / 2, (h - level.height) / 2

        spritepos = {sprite: sprite.pos for sprite in level.sprites}

        redraw_pixels = set(level.cells.keys())
        while True:
            for sprite in spritepos.keys():
                if sprite not in level.sprites:
                    redraw_pixels.add(sprite.pos)
                    del spritepos[sprite]
            for sprite in level.sprites:
                if sprite not in spritepos:
                    redraw_pixels.add(sprite.pos)
                elif sprite.pos != spritepos[sprite]:
                    redraw_pixels.add(spritepos[sprite])
                    redraw_pixels.add(sprite.pos)
                    spritepos[sprite] = sprite.pos

            for cx, cy in redraw_pixels:
                r, g, b = self.get_pixel_colour(level, (cx, cy))
                self.arduino.write_ints(int(cx + ox), int(cy + oy), r, g, b)
            redraw_pixels.clear()

            elapsed = float(self.clock.tick(60))

            keys = []
            # handle events
            for event in pygame.event.get():
                # close window
                if event.type == pygame.QUIT:
                    sys.exit()

                # get keypresses
                elif event.type == pygame.KEYDOWN:
                    keys.append((event.key, True))
                elif event.type == pygame.KEYUP:
                    keys.append((event.key, False))

            events = []
            for key, keydown in keys:
                # skip level
                if keydown and key == pygame.K_RETURN:
                    return True

                # move event
                if key in self.move_keys:
                    events.append(('move', self.move_keys.index(key), keydown))

            level.update_level(events, elapsed)

            if level.check_for_failure():
                return False
            if level.check_for_success():
                return True


    def get_pixel_colour(self, level, (cx, cy)):
        sprites = level.sprites.at((cx, cy))
        return (self.colours[sprites[0].type] if sprites else
                   self.colours[level.cells[cx, cy].type])
