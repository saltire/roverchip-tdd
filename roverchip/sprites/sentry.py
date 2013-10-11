from roverchip.sprite import Sprite


class Sentry(Sprite):
    is_solid = True

    def start_turn(self):
        if not self.to_move and self.level.enemy_can_enter(self.get_pos_in_dir(self.rotate)):
            self.start_move(self.rotate)
