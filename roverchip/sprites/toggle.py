from roverchip.sprite import Sprite


class Toggle(Sprite):
    def __init__(self, level, (x, y), is_solid=True):
        Sprite.__init__(self, level, (x, y))

        self.is_solid = is_solid
