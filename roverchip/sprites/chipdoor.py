from mixins.door import Door
from roverchip.sprite import Sprite


class ChipDoor(Door, Sprite):
    def __init__(self, level, (x, y), rotate=0):
        Sprite.__init__(self, level, (x, y), rotate)

        self.is_solid = True


    def attempt_open(self, player):
        chipquota = getattr(self.level, 'chipquota', 0)
        if len(player.carrying['Chip']) >= chipquota:
            self.is_solid = False
