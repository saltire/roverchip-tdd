from sprite import Sprite


class Key(Sprite):
    def __init__(self, level, (x, y), colour):
        Sprite.__init__(self, level, (x, y))

        self.colour = colour
