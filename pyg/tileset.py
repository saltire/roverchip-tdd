import pygame


class Tileset:
    def __init__(self, tilepath, tilesize):
        self.img = pygame.image.load(tilepath).convert_alpha()

        tw, th = tilesize
        self.dims = self.img.get_width() / tw, self.img.get_height() / th


    def resize_tileset(self, cellsize):
        """Resize the tileset to fit the cell size."""
        self.cellsize = cellsize

        w, h = self.dims
        size = w * cellsize, h * cellsize
        self.tileset = pygame.transform.scale(self.img, size)


    def get_tile(self, (x, y), rotate=0):
        """Return a single tile surface based on coordinates and cell size."""
        tileimg = self.tileset.subsurface((x * self.cellsize, y * self.cellsize,
                                           self.cellsize, self.cellsize))

        return (pygame.transform.rotate(tileimg, rotate * -90) if rotate != 0
                else tileimg)
