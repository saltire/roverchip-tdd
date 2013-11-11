from roverchip.sprite import Sprite
from roverchip.spritegroup import SpriteGroup


class Laser(Sprite):
    is_solid = True

    def __init__(self, level, (x, y), rotate):
        Sprite.__init__(self, level, (x, y), rotate)

        self.beams = SpriteGroup()


    def start_turn(self):
        self.level.sprites -= self.beams
        self.beams.clear()


    def end_turn(self):
        direction = self.rotate
        pos = self.pos

        while True:
            pos = self.level.get_pos_in_dir(pos, direction)

            # stop laser if sprites cannot enter this cell
            # or mirrors in the cell are not fully in the cell
            # or cell contains non-destructible non-mirror solid sprites
            if not (pos in self.level.cells and self.level.cells[pos].sprite_can_enter
                    and all((sprite.pos == pos and sprite.type == 'Mirror')
                            or sprite.is_destructible
                            for sprite in self.level.sprites.solid.on(pos))):
                break

            # change direction if mirror in cell
            mirrors = self.level.sprites['Mirror'].at(pos)
            if mirrors:
                mirror = mirrors.pop()
                # the mirror's two facing directions
                mdirs = mirror.rotate, (mirror.rotate + 1) % 4
                # the facing direction opposite to the laser's entry
                enter_dir = (direction + 2) % 4
                if enter_dir not in mdirs:
                    # not hitting a facing dir of the mirror: stop laser
                    break
                # the other facing direction
                exit_dir = mdirs[(mdirs.index(enter_dir) + 1) % 2]
            else:
                exit_dir = direction

            beam = Laserbeam(self.level, pos, direction, exit_dir)
            self.level.sprites.add(beam)
            self.beams.add(beam)

            # kill destructible sprites in this cell
            for sprite in self.level.sprites.destructible.on(pos):
                sprite.destroy()

            direction = exit_dir


class Laserbeam(Sprite):
    def __init__(self, level, (x, y), rotate, exit_dir):
        Sprite.__init__(self, level, (x, y), rotate)

        self.exit_dir = exit_dir
