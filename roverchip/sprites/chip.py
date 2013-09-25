from roverchip.sprite import Sprite


class Chip(Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))

        self.is_item = True
