from cells import celltypes
from spritegroup import SpriteGroup
from sprites import spritetypes


class Level:
    def __init__(self, celldata, spritedata, animation=True):
        self.cells = {}
        for (x, y), cell in celldata.items():
            celltype, args = cell[0], cell[1:]
            self.cells[x, y] = celltypes[celltype](*args)

        self.width = len(set(x for x, _ in self.cells))
        self.height = len(set(y for _, y in self.cells))

        self.sprites = SpriteGroup()
        for sprite in spritedata:
            spritetype, (x, y), args = sprite[0], sprite[1], sprite[2:]
            self.add_sprite(spritetype, (x, y), *args)

        self.animation = animation


    def add_sprite(self, spritetype, (x, y), *args):
        """Given a sprite type and position, add the sprite."""
        spr = spritetypes[spritetype](self, (x, y), *args)
        self.sprites.add(spr)
        return spr


    def update_level(self, actions, elapsed):
        """Handle action commands and move sprites."""
        for player in self.sprites['Player']:
            # this assumes there is only one player for now
            for action in actions:
                player.handle_action(*action)

        # call sprite hooks
        for sprite in self.sprites.active.by_priority():
            sprite.start_turn()
            sprite.do_move(elapsed)
            if sprite.get_cell():
                sprite.after_move()
        for sprite in self.sprites.active:
            sprite.end_turn()


    def check_for_success(self):
        """Return true if the level has been completed."""
        pass


    def check_for_failure(self):
        """Return true if the level has been failed."""
        pass


    def get_cell_type(self, (x, y)):
        """If a cell exists at the given position, return its type."""
        cell = self.cells.get((x, y), None)
        return cell.get_type() if cell is not None else None


    def sprite_can_enter(self, (x, y)):
        """Return true if cell exists, doesn't contain solid sprites,
        and doesn't specify no sprites."""
        return ((x, y) in self.cells
                and not self.sprites.solid.on((x, y))
                and self.cells[x, y].sprite_can_enter
                )


    def robot_can_enter(self, (x, y)):
        """Return true if sprites can enter the cell,
        and it doesn't specify no robots."""
        return (self.sprite_can_enter((x, y)) and self.cells[x, y].robot_can_enter)


    def player_can_enter(self, (x, y)):
        """Return true if cell exists, doesn't contain solid immovable sprites
        or solid sprites partially in the cell (except Rover), and doesn't specify no player.
        If the cell is water, there must be a bridge sprite completely in it."""
        return ((x, y) in self.cells
                and (self.cells[x, y].player_can_enter
                     or (self.cells[x, y].get_type() == 'Water'
                         and self.sprites.bridge.on((x, y))))
                and all((spr.is_movable and spr.get_cell()) or spr.get_type() == 'Rover'
                        for spr in self.sprites.solid.on((x, y)))
                )
