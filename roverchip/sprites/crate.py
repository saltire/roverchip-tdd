from sprite import Sprite


class Crate(Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))

        self.is_movable = True
        self.is_solid = True


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
                    and not self.level.sprites_at(nextcell)):
                    self.move_dir = flow_dir
                    self.to_move = 1
