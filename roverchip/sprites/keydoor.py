from mixins.door import Door
from roverchip.sprite import Sprite


class KeyDoor(Door, Sprite):
    def __init__(self, level, (x, y), rotate=0, colour=0):
        Sprite.__init__(self, level, (x, y), rotate)

        self.colour = colour


    def attempt_open(self, player):
        for key in player.carrying['Key'].active:
            if key.colour == self.colour:
                self.is_solid = False
                key.is_active = False
                player.carrying.remove(key)
                break
