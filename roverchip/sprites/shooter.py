from roverchip.sprite import Sprite


class Shooter(Sprite):
    tile_rotates = True
    is_destructible = True
    is_solid = True

    def end_turn(self):
        """Kill any players or Rovers in the shooter's line of sight."""
        distance = 1
        while True:
            pos = self.get_pos_in_dir(self.rotate, distance)
            # stop projectile if sprites can't enter this cell
            # or solid sprites other than player or rover are in the cell
            if not (pos in self.level.cells and self.level.cells[pos].sprite_can_enter
                    and all(sprite.type in ('Player', 'Rover')
                            for sprite in self.level.sprites.solid.on(pos))):
                break
            for sprite in self.level.sprites['Player', 'Rover'].at(pos):
                sprite.destroy()
            distance += 1
