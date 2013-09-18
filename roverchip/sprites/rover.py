from sprite import Sprite


class Rover(Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))

        self.is_solid = True
