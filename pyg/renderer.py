class Renderer:
    tiles = {
             'Exit': (6, 0),
             'Fire': (2, 0),
             'Floor': (0, 0),
             'Grate': (5, 0),
             'Wall': (1, 0),

             'Chip': (7, 2),
             'Crate': (2, 1),
             'Laser': (4, 1),
             'Mirror': (7, 1),
             'Player': (0, 2),
             'Robot': (3, 2),
             'Rover': (1, 2),
             'Sentry': (3, 3),
             'SentryButton': (9, 3),
             'Shooter': (2, 2),
             'ToggleButton': (9, 2),
             }

    layers = {
              'Chip':-1,
              'Key': 2,
              'Laserbeam':-1,
              'Player': 1,
              'Rover': 1,
              }

    def __init__(self, tileset):
        self.tileset = tileset


    def render(self, obj):
        """Return the tile corresponding to the cell/sprite type,
        or find it according to special instructions if they exist."""
        tilemethod = '_render_' + obj.type.lower()
        return (getattr(self, tilemethod)(obj) if hasattr(self, tilemethod)
                else self.tileset.get_tile(self.tiles[obj.type], obj.rotate))


    def get_layer(self, sprite):
        """Return the layer of the corresponding sprite,
        or find it according to special instructions if they exist."""
        layermethod = '_layer_' + sprite.type.lower()
        return (getattr(self, layermethod)(sprite) if hasattr(self, layermethod)
                else self.layers.get(sprite.type, 0))


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


    def _render_key(self, key):
        """Return a key tile of the correct colour."""
        return self.tileset.get_tile((6, 2 + key.colour))


    def _render_keydoor(self, keydoor):
        """Return a door tile of the correct colour."""
        if keydoor.is_solid:
            return self.tileset.get_tile((5, 2 + keydoor.colour), keydoor.rotate)
        else:
            return None


    def _render_laserbeam(self, beam):
        """Return a rotated laser tile, bending in the correct direction if necessary."""
        if beam.exit_dir == beam.rotate:
            return self.tileset.get_tile((5, 1), beam.rotate)
        else:
            rotate_mod = 0 if (beam.exit_dir - beam.rotate) % 4 == 1 else 1
            return self.tileset.get_tile((6, 1), (beam.rotate + rotate_mod) % 4)


    def _render_toggle(self, toggle):
        """If the toggle is solid, return a toggle outline superimposed a wall tile;
        otherwise just return a toggle outline."""
        toggle_tile = self.tileset.get_tile((11, 0))
        if toggle.is_solid:
            wall_tile = self.tileset.get_tile((1, 0)).copy()
            wall_tile.blit(toggle_tile, (0, 0))
            return wall_tile
        else:
            return toggle_tile


    def _render_water(self, water):
        """Rotate and return the flowing water tile if a flow direction is set,
        otherwise return the still water tile."""
        if water.flow_dir is None:
            return self.tileset.get_tile((3, 0))
        else:
            return self.tileset.get_tile((4, 0), water.flow_dir)
