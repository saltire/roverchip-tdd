class Sprite:
    def __init__(self, level, (x, y), facing=0):
        self.level = level
        
        # initial values
        self.pos = x, y                 # sprite's coords on cell grid
        self.facing = facing            # direction sprite is facing
        self.tile_facing = facing       # direction tile is facing
        self.to_move = 0, 0             # distance left to move, and direction
        
        # defaults to override
        self.tile = 0, 0                # coords of sprite's tile in tileset
        self.layer = 0                  # layer the sprite is rendered on
        self.size = 1                   # size of sprite in cells
        self.speed = 4                  # cells moved per second
        self.rotate = False             # tile rotates according to self.facing


    def get_type(self):
        """Return the type of the sprite, i.e. the class name."""
        return self.__class__.__name__
    
    
    def _get_dest_pos(self, direction, distance=1):
        """Given a direction and an optional distance, give the position
        after travelling that distance in that direction."""
        x, y = self.pos
        distance *= -1 if direction in [0, 3] else 1 # negative if N or W
        return (x + distance, y) if direction % 2 else (x, y + distance)


    def start_move(self, direction):
        """Start the sprite moving one cell in the given direction."""
        if self.level.sprite_can_enter(self._get_dest_pos(direction)):
            self.to_move = 1, direction
        
        
    def do_move(self, elapsed):
        """Move the sprite based on how much time has elapsed."""
        remaining, direction = self.to_move
        if remaining:
            distance = min(self.speed * (elapsed / 1000.0), remaining)
            self.to_move = remaining - distance, direction
            self.pos = self._get_dest_pos(direction, distance)
            
            