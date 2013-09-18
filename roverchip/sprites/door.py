from sprite import Sprite


class Door(Sprite):
    def __init__(self, level, (x, y), rotate, colour):
        Sprite.__init__(self, level, (x, y), rotate)

        self.is_solid = True

        self.colour = colour
