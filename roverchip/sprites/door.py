from roverchip.sprite import Sprite


class Door(Sprite):
    def __init__(self, level, (x, y), rotate=0, colour=0):
        Sprite.__init__(self, level, (x, y), rotate)

        self.is_solid = True

        self.colour = colour
