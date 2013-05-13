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
    
    
    def sprite_can_enter(self, (x, y)):
        return (x, y) in self.cells