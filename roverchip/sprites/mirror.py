from roverchip.sprite import Sprite
from roverchip.sprites.mixins.movable import Movable


class Mirror(Movable, Sprite):
    is_solid = True
