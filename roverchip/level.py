from cells import celltypes
from sprites import spritetypes


class Level:
    def __init__(self, celldata, spritedata, animation=True):
        self.cells = {}
        for (x, y), cell in celldata.items():
            celltype, args = cell[0], cell[1:]
            self.cells[x, y] = celltypes[celltype](*args)

        self.width = len(set(x for x, _ in self.cells))
        self.height = len(set(y for _, y in self.cells))

        self.sprites = set()
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
        for player in self.sprites_by_type('Player'):
            # this assumes there is only one player for now
            for action in actions:
                player.handle_action(*action)

        for spr in self.sprites:
            spr.start_turn()
        for spr in self.sprites:
            spr.do_move(elapsed)
            if spr.get_cell():
                spr.after_move()


    def handle_action(self, etype, *args):
        """Given some events, take the necessary actions."""
        if etype == 'move':
            player = self.sprites_by_type('Player')[0]
            player.handle_move_event(*args)


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


    def sprites_by_type(self, stype):
        """Return all sprites whose type matche the given string."""
        return set(spr for spr in self.sprites if spr.get_type() == stype)


    def sprites_at(self, (x, y), stype=None):
        """Return all sprites at the given position.
        Optionally filter by sprite type."""
        return set(spr for spr in self.sprites if spr.pos == (x, y)
                   and (stype is None or stype == spr.get_type()))


    def movables_at(self, (x, y), stype=None):
        """Return all movable sprites at the given position.
        Optionally filter by sprite type."""
        return set(spr for spr in self.sprites_at((x, y), stype) if spr.is_movable)


    def solids_at(self, (x, y), stype=None):
        """Return all solid sprites at the given position.
        Optionally filter by sprite type."""
        return set(spr for spr in self.sprites_at((x, y), stype) if spr.is_solid)


    def sprites_in(self, (x, y), stype=None):
        """Return all sprites overlapping the cell at the given position.
        Optionally filter by sprite type."""
        return set(spr for spr in self.sprites if
                   x - spr.size < spr.pos[0] < x + 1 and
                   y - spr.size < spr.pos[1] < y + 1 and
                   (stype is None or stype == spr.get_type()))


    def movables_in(self, (x, y), stype=None):
        """Return all movable sprites overlapping the cell at the given pos.
        Optionally filter by sprite type."""
        return set(spr for spr in self.sprites_in((x, y), stype) if spr.is_movable)


    def solids_in(self, (x, y), stype=None):
        """Return all solid sprites overlapping the cell at the given pos.
        Optionally filter by sprite type."""
        return set(spr for spr in self.sprites_in((x, y), stype) if spr.is_solid)


    def sprite_can_enter(self, (x, y)):
        """Return true if cell exists, doesn't contain solid sprites,
        and doesn't specify no sprites."""
        return ((x, y) in self.cells
                and self.cells[x, y].sprite_can_enter
                and not self.solids_at((x, y))
                )


    def robot_can_enter(self, (x, y)):
        """Return true if sprites can enter the cell,
        and it doesn't specify no robots."""
        return (self.sprite_can_enter((x, y))
                and self.cells[x, y].robot_can_enter
                )


    def player_can_enter(self, (x, y)):
        """Return true if cell exists, doesn't contain solid immovable sprites
        or solid sprites partially in the cell, and doesn't specify no player.
        If the cell is water, there must be a bridge sprite completely in it."""
        return ((x, y) in self.cells
                and (self.cells[x, y].player_can_enter
                     or (self.cells[x, y].get_type() == 'Water'
                         and any(spr.is_bridge for spr in self.sprites_in((x, y)))))
                and all(spr.is_movable and spr.get_cell() for spr in self.solids_at((x, y)))
                )
