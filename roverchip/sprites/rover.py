from roverchip.sprite import Sprite


class Rover(Sprite):
    tile_rotates = True
    is_destructible = True
    is_solid = True

    def end_turn(self):
        """Kill Rover if he is overlapping any enemies."""
        if self.level.sprites.enemy.on(self.pos):
            self.destroy()
