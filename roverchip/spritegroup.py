import operator


class SpriteGroup(set):
    def __getattr__(self, attr):
        """Return all sprites in the group for which there is a flag
        set with the given attribute, e.g. group.active returns all
        sprites for which sprite.is_active is true."""
        return SpriteGroup(sprite for sprite in self if getattr(sprite, 'is_' + attr))


    def __getitem__(self, types):
        """Return all sprites in the group of the given type(s).
        If passed None, return all sprites."""
        return SpriteGroup(sprite for sprite in self
                           if types is None or sprite.get_type() in types)


    def at(self, *positions):
        """Return all sprites with the exact given coordinates.
        Can take more than one set of coordinates."""
        return SpriteGroup(sprite for sprite in self if sprite.pos in positions)


    def on(self, *positions):
        """Return all sprites overlapping the 1x1 square at the given coordinates.
        Can take more than one set of coordinates."""
        return SpriteGroup(sprite for sprite in self if
                           any(x - 1 < sprite.pos[0] < x + 1 and y - 1 < sprite.pos[1] < y + 1
                               for x, y in positions))


    def by_layer(self):
        """Return a list of sprites sorted by increasing layer."""
        return sorted(self, key=operator.attrgetter('layer'))


    def by_priority(self):
        """Return a list of sprites sorted by decreasing priority."""
        return sorted(self, key=operator.attrgetter('priority'), reverse=True)
