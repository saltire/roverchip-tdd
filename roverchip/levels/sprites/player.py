from sprite import Sprite


class Player(Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))
        
        self.pushing = set()               # sprites being pushed
        
    
    def start_move(self, direction):
        """Start the player moving, and push movable objects."""
        nextpos = self._get_dest_pos(direction)
        
        if self.level.player_can_enter(nextpos):
            movables = self.level.movables_at(nextpos)
            if (not movables or
                (movables and not
                 self.level.solids_at(movables[0]._get_dest_pos(direction)))):
                self.to_move = 1
                self.move_dir = direction
                if movables:
                    self.pushing |= set(movables)
                    
    
    def do_move(self, elapsed):
        """Move the player and also move pushed sprites."""
        distance = Sprite.do_move(self, elapsed)
        
        for spr in self.pushing.copy():
            spr.pos = spr._get_dest_pos(self.move_dir, distance)
            if self.to_move == 0:
                self.pushing.discard(spr)
        