class CellRenderer:
    tiles = {'Floor': (0, 0),
             'Grate': (5, 0)
             }
    
    
    def __init__(self, tileset):
        self.tileset = tileset
        
        
    def render_cell(self, cell):
        """Return the tile corresponding to the cell type, or render it
        according to special instructions."""
        methodname = 'render_{0}'.format(cell.get_type().lower())
        return (getattr(self, methodname)(cell) if hasattr(self, methodname)
                else self.tileset.get_tile(self.tiles[cell.get_type()]))
