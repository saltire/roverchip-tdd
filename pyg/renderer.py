class Renderer:
    tiles = {'Floor': (0, 0),
             'Grate': (5, 0),
             
             'Player': (0, 2),
             'Crate': (2, 1)
             }
    
    
    def __init__(self, tileset):
        self.tileset = tileset
        
        
    def render(self, obj):
        """Return the tile corresponding to the cell/sprite type, or render it
        according to special instructions."""
        methodname = 'render_{0}'.format(obj.get_type().lower())
        return (getattr(self, methodname)(obj) if hasattr(self, methodname)
                else self.tileset.get_tile(self.tiles[obj.get_type()],
                                           obj.rotate))
