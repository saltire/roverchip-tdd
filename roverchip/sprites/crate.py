from sprite import Sprite


class Crate(Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))

        self.is_movable = True
        self.is_solid = True
