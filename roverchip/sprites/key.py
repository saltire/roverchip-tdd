from roverchip.sprite import Sprite


class Key(Sprite):
    is_item = True

    def __init__(self, level, (x, y), colour=0):
        Sprite.__init__(self, level, (x, y))

        self.colour = colour
