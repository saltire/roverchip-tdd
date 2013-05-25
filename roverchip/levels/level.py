from cells import celltypes
from sprites import spritetypes


class Level:
    def __init__(self, celldata, spritedata):
        self.cells = {}
        for (x, y), cell in celldata.items():
            celltype, args = cell[0], cell[1:]
            self.cells[x, y] = celltypes[celltype](*args)

        self.width = len(set(x for x, _ in self.cells))
        self.height = len(set(y for _, y in self.cells))
        
        self.sprites = []
        for sprite in spritedata:
            spritetype, (x, y), args = sprite[0], sprite[1], sprite[2:]
            self.add_sprite(spritetype, (x, y), *args)
            
            
    def add_sprite(self, spritetype, (x, y), *args):
        """Given a sprite type and position, add the sprite."""
        spr = spritetypes[spritetype](self, (x, y), *args)
        self.sprites.append(spr)
        return spr
            
            
    def handle_event(self, etype, *args):
        """Given some events, take the necessary actions."""
        if etype == 'move':
            player = self.sprites_by_type('Player')[0]
            player.attempt_move(args[0])
            
            
    def update_level(self, elapsed):
        """Move sprites and take any resulting actions."""
        for spr in self.sprites:
            spr.do_move(elapsed)
            
            
    def check_for_success(self):
        """Return true if the level has been completed."""
        pass


    def check_for_failure(self):
        """Return true if the level has been failed."""
        pass
    
    
    def sprites_by_type(self, stype):
        """Return all sprites whose type matche the given string."""
        return [spr for spr in self.sprites if spr.get_type() == stype]
            
            
    def sprites_at(self, (x, y)):
        """Return all sprites at the given position."""
        return [spr for spr in self.sprites if spr.pos == (x, y)]
    
    
    def movables_at(self, (x, y)):
        """Return all movable sprites at the given position."""
        return [spr for spr in self.sprites_at((x, y)) if spr.is_movable]
    
    
    def solids_at(self, (x, y)):
        """Return all solid sprites at the given position."""
        return [spr for spr in self.sprites_at((x, y)) if spr.is_solid]
    
    
    def sprites_in(self, (x, y)):
        """Return all sprites overlapping the cell at the given position."""
        return [spr for spr in self.sprites if
                x - spr.size < spr.pos[0] < x + 1 and
                y - spr.size < spr.pos[1] < y + 1]
    
    
    def movables_in(self, (x, y)):
        """Return all movable sprites overlapping the cell at the given pos."""
        return [spr for spr in self.sprites_in((x, y)) if spr.is_movable]
    
    
    def solids_in(self, (x, y)):
        """Return all solid sprites overlapping the cell at the given pos."""
        return [spr for spr in self.sprites_in((x, y)) if spr.is_solid]
    
    
    def sprite_can_enter(self, (x, y)):
        """Return true if cell exists and doesn't contain solid sprites."""
        return ((x, y) in self.cells
                and self.cells[x, y].sprite_can_enter
                and not self.solids_at((x, y))
                )


    def player_can_enter(self, (x, y)):
        """Return true if cell exists and doesn't contain solid immovable
        sprites."""
        return ((x, y) in self.cells
                and self.cells[x, y].sprite_can_enter
                and all(spr.is_movable for spr in self.solids_at((x, y)))
                )