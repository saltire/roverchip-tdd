class Renderer:
    tiles = {
             'Exit': (6, 0),
             'Floor': (0, 0),
             'Grate': (5, 0),
             'Wall': (1, 0),

             'Chip': (7, 2),
             'Crate': (2, 1),
             'Player': (0, 2),
             'Robot': (3, 2),
             'Rover': (1, 2),
             }

    def __init__(self, tileset):
        self.tileset = tileset


    def render(self, obj):
        """Return the tile corresponding to the cell/sprite type, or render it
        according to special instructions."""
        methodname = 'render_{0}'.format(obj.get_type().lower())
        return (getattr(self, methodname)(obj) if hasattr(self, methodname)
                else self.tileset.get_tile(self.tiles[obj.get_type()], obj.rotate))


    def render_chipdoor(self, chipdoor):
        """Return a tile of the correct rotation."""
        if chipdoor.is_solid:
            return self.tileset.get_tile((7, 4) if chipdoor.rotate % 2 else (7, 3))
        else:
            return None


    def render_crate(self, crate):
        """Return either a regular or sunken crate tile."""
        return self.tileset.get_tile((3, 1) if crate.is_bridge else (2, 1))


    def render_door(self, door):
        """Return a door tile of the correct colour."""
        if door.is_solid:
            return self.tileset.get_tile((5, 2 + door.colour), door.rotate)
        else:
            return None


    def render_key(self, key):
        """Return a key tile of the correct colour."""
        return self.tileset.get_tile((6, 2 + key.colour))


    def render_water(self, water):
        """Rotate and return the flowing water tile if a flow direction is set,
        otherwise return the still water tile."""
        if water.flow_dir is None:
            return self.tileset.get_tile((3, 0))
        else:
            return self.tileset.get_tile((4, 0), water.flow_dir)
