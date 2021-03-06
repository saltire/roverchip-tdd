from roverchip.sprite import Sprite
from roverchip.sprites.mixins.movable import Movable


class Crate(Movable, Sprite):
    is_solid = True

    def start_turn(self):
        if not self.is_bridge and self.get_cell_type() == 'Water':
            # sink into the water
            self.is_bridge = True
            self.is_movable = False
            self.is_solid = False

        cell = self.get_cell()
        if self.is_bridge and cell is not None:
            # start moving if possible
            flow_dir = cell.flow_dir
            if flow_dir is not None:
                nextcell = self.get_pos_in_dir(flow_dir)
                if (self.level.get_cell_type(nextcell) == 'Water'
                    and not self.level.sprites.at(nextcell)):
                    self.move_dir = flow_dir
                    self.to_move = 1
