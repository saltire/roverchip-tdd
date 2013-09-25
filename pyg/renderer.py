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

    layers = {
              'Key': 2,
              'Player': 1,
              'Rover': 1,
              }

    def __init__(self, tileset):
        self.tileset = tileset


    def render(self, obj):
        """Return the tile corresponding to the cell/sprite type,
        or find it according to special instructions if they exist."""
        tilemethod = '_render_' + obj.get_type().lower()
        return (getattr(self, tilemethod)(obj) if hasattr(self, tilemethod)
                else self.tileset.get_tile(self.tiles[obj.get_type()], obj.rotate))


    def get_layer(self, sprite):
        """Return the layer of the corresponding sprite,
        or find it according to special instructions if they exist."""
        layermethod = '_layer_' + sprite.get_type().lower()
        return (getattr(self, layermethod)(sprite) if hasattr(self, layermethod)
                else self.layers.get(sprite.get_type(), 0))


    def _layer_crate(self, crate):
        """Layer below other sprites if in water."""
        return -1 if crate.is_bridge else 0


    def _layer_dirt(self, dirt):
        """Layer below other sprites if in water."""
        return -1 if dirt.is_bridge else 0


    def _render_chipdoor(self, chipdoor):
        """Return a tile of the correct rotation."""
        if chipdoor.is_solid:
            return self.tileset.get_tile((7, 4) if chipdoor.rotate % 2 else (7, 3))
        else:
            return None


    def _render_crate(self, crate):
        """Return either a regular or sunken crate tile."""
        return self.tileset.get_tile((3, 1) if crate.is_bridge else (2, 1))


    def _render_dirt(self, dirt):
        """Return a dirt tile, a mud tile, or a regular floor tile."""
        if not dirt.is_bridge:
            return self.tileset.get_tile((8, 1)) # dirt
        elif dirt.is_solid:
            return self.tileset.get_tile((8, 0)) # mud
        else:
            return self.tileset.get_tile((0, 0)) # floor


    def _render_door(self, door):
        """Return a door tile of the correct colour."""
        if door.is_solid:
            return self.tileset.get_tile((5, 2 + door.colour), door.rotate)
        else:
            return None


    def _render_key(self, key):
        """Return a key tile of the correct colour."""
        return self.tileset.get_tile((6, 2 + key.colour))


    def _render_water(self, water):
        """Rotate and return the flowing water tile if a flow direction is set,
        otherwise return the still water tile."""
        if water.flow_dir is None:
            return self.tileset.get_tile((3, 0))
        else:
            return self.tileset.get_tile((4, 0), water.flow_dir)
