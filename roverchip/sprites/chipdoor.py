from roverchip.sprite import Sprite


class ChipDoor(Sprite):
    def __init__(self, level, (x, y), rotate=0):
        Sprite.__init__(self, level, (x, y), rotate)

        self.is_solid = True
