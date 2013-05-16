from cells import celltypes
from sprites import spritetypes


class Level:
    def __init__(self, celldata, spritedata):
        self.cells = {}
        for (x, y), celltype in celldata.items():
            self.cells[x, y] = celltypes[celltype]()

        self.sprites = []
        for spritetype, (x, y) in spritedata:
            self.sprites.append(spritetypes[spritetype](self, (x, y)))
            
            
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
                x - 1 < spr.pos[0] < x + 1 and
                y - 1 < spr.pos[1] < y + 1]
    
    
    def movables_in(self, (x, y)):
        """Return all movables sprites overlapping the cell at the given pos."""
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