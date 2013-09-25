from roverchip.sprite import Sprite


class Key(Sprite):
    def __init__(self, level, (x, y), colour=0):
        Sprite.__init__(self, level, (x, y))

        self.is_item = True

        self.colour = colour
