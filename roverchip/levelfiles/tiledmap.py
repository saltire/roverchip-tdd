import struct
import zlib

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

from levelfile import LevelFile


class TiledMap(LevelFile):
    tiles = {
             (0, 0): ('Floor',),
             (1, 0): ('Wall',),
             (2, 0): ('Water',),
             (3, 0): ('Conveyor', ''),
             (4, 0): ('Ice',),
             (5, 0): ('Toggle', 0),
             (6, 0): ('Button', 0),
             (7, 0): ('Door', '', 0),
             (8, 0): ('Door', '', 1),
             (9, 0): ('Door', '', 2),
             (10, 0): ('Door', '', 3),
             (11, 0): ('ChipDoor', ''),
             (0, 1): ('Grate',),
             (1, 1): ('Fire',),
             (2, 1): ('Water', ''),
             (4, 1): ('Ice', ''),
             (5, 1): ('Toggle', 1),
             (6, 1): ('Button', 1),
             (0, 2): ('Exit',),
             (1, 2): ('Mud',),
             (0, 4): ('Ball',),
             (1, 4): ('Cart',),
             (2, 4): ('Crate',),
             (3, 4): ('Laser', ''),
             (4, 4): ('Mirror', ''),
             (5, 4): ('Dirt',),
             (7, 4): ('Key', 0),
             (8, 4): ('Key', 1),
             (9, 4): ('Key', 2),
             (10, 4): ('Key', 3),
             (11, 4): ('Chip',),
             (0, 5): ('Player',),
             (1, 5): ('Rover',),
             (2, 5): ('Shooter', ''),
             (3, 5): ('Robot', '', 0),
             (4, 5): ('Tank', '', 1),
             (5, 5): ('Sentry', ''),
             (7, 5): ('Boots', 0),
             (8, 5): ('Boots', 1),
             (9, 5): ('Boots', 2),
             (10, 5): ('Boots', 3),
             (3, 6): ('Robot', '', 1),
             (4, 6): ('Tank', '', 2),
             }

    def __init__(self, path):
        with open(path, 'rb') as lfile:
            self.xmldata = etree.fromstring(lfile.read())

        self.properties = {prop.attrib['name']: prop.attrib['value']
                           for prop in self.xmldata.findall('properties/property')}


    def get_data(self):
        """Parse the data as a Tiled XML level file.
        Get cell data from the first layer and sprite data from the rest."""
        width = int(self.xmldata.get('width'))
        height = int(self.xmldata.get('height'))
        layers = self.xmldata.findall('layer')

        # interpret bottom layer as tiles
        celldata = self._get_tile_data(layers[0], width, height)

        # interpret all subsequent layers as sprites
        spritedata = []
        for layer in layers[1:]:
            spritetiles = self._get_tile_data(layer, width, height)
            for (x, y), sdata in spritetiles.items():
                spritedata.append([sdata[0], (x, y)] + sdata[1:])

        return celldata, spritedata


    def _get_tile_data(self, layer, width, height):
        """Get tile types and rotation from raw layer data."""
        layerdata = self._get_layer_data(layer)
        tiledata = {}
        for y in range(height):
            for x in range(width):
                tile = layerdata[y * width + x]
                if tile:
                    tilenum = tile % 0x10000000 - 1
                    tiletype = self.tiles[tilenum % 16, tilenum / 16]
                    rotate = (0, 10, 12, 6).index(tile / 0x10000000)
                    # replace empty string in tile properties with rotation value
                    tiledata[x, y] = [(rotate if prop == '' else prop) for prop in tiletype]
        return tiledata


    def _get_layer_data(self, layer):
        """Read raw layer data saved by Tiled, in any of several formats."""
        data = layer.find('data')
        encoding = data.get('encoding')
        compression = data.get('compression')

        if encoding is None:
            return [int(tile.get('gid')) for tile in data.findall('tile')]

        elif encoding == 'csv':
            return [int(i.strip()) for i in data.text.split(',')]

        elif encoding == 'base64':
            if compression is None:
                bdata = data.text.strip().decode('base64')
            elif compression == 'gzip':
                bdata = zlib.decompress(data.text.strip().decode('base64'), 47)
            elif compression == 'zlib':
                bdata = zlib.decompress(data.text.strip().decode('base64'))

            return [struct.unpack('I', bdata[i:i + 4])[0]
                    for i in range(0, len(bdata), 4)]
