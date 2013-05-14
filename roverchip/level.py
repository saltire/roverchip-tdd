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
        """Return all sprites at the given position."""
        return [spr for spr in self.sprites if spr.pos == (x, y) and spr.is_movable]
    
    
    def solids_at(self, (x, y)):
        """Return all sprites at the given position."""
        return [spr for spr in self.sprites if spr.pos == (x, y) and spr.is_solid]
    
    
    def sprite_can_enter(self, (x, y)):
        return ((x, y) in self.cells
                and self.cells[x, y].sprite_can_enter
                and not self.solids_at((x, y))
                )


    def player_can_enter(self, (x, y)):
        return ((x, y) in self.cells
                and self.cells[x, y].sprite_can_enter
                and all(spr.is_movable for spr in self.solids_at((x, y)))
                )