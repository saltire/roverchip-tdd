from roverchip.sprite import Sprite


class Dirt(Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))

        self.is_movable = True
        self.is_solid = True


    def start_turn(self):
        # sink when over water without an existing bridge
        if (not self.is_bridge and self.get_cell_type() == 'Water'
            and not self.level.sprites.bridge.at(self.pos)):
            self.is_bridge = True
            self.is_movable = False

        # clear away mud when player steps on this cell
        if self.is_bridge and self.level.sprites['Player'].at(self.pos):
            self.is_solid = False
