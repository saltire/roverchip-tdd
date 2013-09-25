from roverchip.sprite import Sprite


class Rover(Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))

        self.tile_rotates = True
        self.layer = 1

        self.is_solid = True
