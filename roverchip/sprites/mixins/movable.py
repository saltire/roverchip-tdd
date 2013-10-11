from roverchip.sprite import Sprite


class Movable:
    is_movable = True

    def after_move(self):
        """After moving onto fire, keep moving in the same direction if possible."""
        if (self.get_cell_type() == 'Fire'
            and self.level.sprite_can_enter(self.get_pos_in_dir(self.move_dir))):
            self.to_move = 1

        Sprite.after_move(self)
