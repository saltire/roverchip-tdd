class Sprite:
    # default properties to override
    priority = 0            # higher value means hooks are called sooner
    size = 1                # size of sprite in cells
    speed = 4               # cells moved per second
    tile_rotates = False    # tile rotates according to movement
    is_active = True        # whether the sprite is in the game
    is_bridge = False       # allows the player to cross water
    is_enemy = False        # kills the player on touch
    is_item = False         # can be picked up by player
    is_movable = False      # can be pushed by player
    is_solid = False        # blocks sprites from entering

    def __init__(self, level, (x, y), rotate=0):
        self.type = self.__class__.__name__
        self.types = set(base.__name__ for base in self.__class__.__bases__) | set([self.type])

        self.level = level

        # initial values
        self.pos = x, y             # sprite's coords on cell grid
        self.rotate = rotate        # rotation of the tile
        self.to_move = 0            # distance left to move
        self.move_dir = 0           # direction sprite is moving
        self.delay_left = 0         # time before sprite can move again


    def get_cell(self):
        """If the sprite is completely inside a cell, return the cell."""
        return self.level.cells.get(self.pos, None)


    def get_cell_type(self):
        """If the sprite is completely inside a cell, return the cell type."""
        cell = self.get_cell()
        return cell.type if cell is not None else None


    def get_pos_in_dir(self, direction, distance=1):
        """Given a direction and an optional distance, give the position
        after travelling that distance in that direction."""
        x, y = self.pos
        distance *= -1 if direction in [0, 3] else 1  # negative if N or W
        # round to avoid floating-point errors
        return ((round(x + distance, 5), y) if direction % 2 else
                (x, round(y + distance, 5)))


    def get_dir_of_pos(self, (dx, dy)):
        """Given a position, give the direction that position is in
        relative to the current position, or None if it does not lie
        in a straight line in a cardinal direction."""
        x, y = self.pos
        try:
            return ((dx == x and dy < y),
                    (dx > x and dy == y),
                    (dx == x and dy > y),
                    (dx < x and dy == y)).index(True)
        except ValueError:
            return None


    def start_move(self, direction):
        """Start the sprite moving one cell in the given direction."""
        self.to_move = 1
        self.move_dir = direction
        if self.tile_rotates:
            self.rotate = direction


    def start_turn(self):
        """This hook is called at the beginning of each frame."""
        pass


    def do_move(self, elapsed):
        """Move the sprite based on how much time has elapsed,
        and return distance moved."""
        distance = 0

        if self.level.animation and self.to_move:
            # cells/s * elapsed ms / 1000 = cells travelled
            distance = min(self.speed * elapsed / 1000.0, self.to_move)
        else:
            if self.to_move and elapsed > self.delay_left:
                distance = self.to_move
                # 1000 ms / cells/s [= ms/cell] * cells = ms delay to add
                self.delay_left += 1000 / self.speed * distance
            self.delay_left = max(self.delay_left - elapsed, 0)

        if distance:
            self.to_move -= distance
            self.pos = self.get_pos_in_dir(self.move_dir, distance)

        return distance


    def after_move(self):
        """This hook is called after a sprite arrives in a new cell."""


    def end_turn(self):
        """This hook is called at the end of each frame."""
        pass
