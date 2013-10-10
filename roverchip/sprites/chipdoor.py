from mixins.door import Door
from roverchip.sprite import Sprite


class ChipDoor(Door, Sprite):
    def attempt_open(self, player):
        chipquota = getattr(self.level, 'chipquota', 0)
        if len(player.carrying['Chip']) >= chipquota:
            self.is_solid = False
