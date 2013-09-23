from sprite import Sprite


class Robot(Sprite):
    def __init__(self, level, (x, y), rotate=0, follow_dir=0):
        Sprite.__init__(self, level, (x, y), rotate)

        self.tile_rotates = True
        self.is_enemy = True
        self.is_solid = True

        self.follow_dir = follow_dir  # 0 to follow left wall, 1 to follow right wall


    def start_turn(self):
        if not self.to_move:
            for turns in (1, 0, -1, -2):
                new_dir = (self.rotate + (turns if self.follow_dir else -turns)) % 4
                if self.level.robot_can_enter(self.get_pos_in_dir(new_dir)):
                    self.start_move(new_dir)
                    break
