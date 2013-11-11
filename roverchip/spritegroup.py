class SpriteGroup(set):
    def __getattr__(self, attr):
        """Return all sprites in the group for which the given is_ flag
        is True. If the attribute starts with not_, return all sprites
        for which the is_ flag is False."""
        target = True
        if attr[:4] == 'not_':
            target = False
            attr = attr[4:]
        return SpriteGroup(sprite for sprite in self if getattr(sprite, 'is_' + attr) == target)


    def __getitem__(self, types):
        """Return all sprites in the group of the given type(s).
        If passed None, return all sprites."""
        if isinstance(types, basestring):
            types = (types,)
        return SpriteGroup(sprite for sprite in self
                           if types is None or sprite.types & set(types))


    def subset(self, sprites=[]):
        """Return a sprite group that is a subset of this group and will
        only return sprites that are also in this group."""
        return SpriteGroupSubset(self, sprites)


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
        return sorted(self, key=lambda spr: spr.layer)


    def by_priority(self):
        """Return a list of sprites sorted by decreasing priority."""
        return sorted(self, key=lambda spr: spr.priority, reverse=True)



class SpriteGroupSubset(SpriteGroup):
    def __init__(self, parent, sprites=[]):
        SpriteGroup.__init__(self, sprites)
        self.parent = parent


    def __iter__(self):
        """Iterate over sprites in both this group and the parent group."""
        return iter(self.parent & set(self))


    def __contains__(self, sprite):
        """Return true if the sprite is in this group and the parent group."""
        return set.__contains__(self, sprite) and sprite in self.parent
