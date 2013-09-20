from sprite import Sprite


class Player(Sprite):
    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))

        self.tile_rotates = True
        self.layer = 1

        self.pushing = set()                # sprites being pushed
        self.move_key_queue = []            # current move key being pressed


    def handle_action(self, etype, *args):
        """Given some action commands, take the necessary actions."""
        if etype == 'move':
            self.handle_move_action(*args)


    def handle_move_action(self, direction, keydown=True):
        """Set or clear the current direction key, depending on whether
        there is a direction key set already."""
        # move key pressed - set key
        if keydown and direction not in self.move_key_queue:
            self.move_key_queue.append(direction)

        # move key released - reset key
        elif not keydown and direction in self.move_key_queue:
            self.move_key_queue.remove(direction)


    def start_turn(self):
        """Start the player moving if stopped and key is down."""
        if (self.move_key_queue and not self.to_move and not self.delay_left):
            self.attempt_move(self.move_key_queue[0])


    def attempt_move(self, direction):
        """Start the player moving, and push movable objects."""
        self.rotate = direction

        nextpos = self._get_dest_pos(direction)
        if self.level.player_can_enter(nextpos):
            movables = self.level.movables_at(nextpos)
            # proceed only if no movables or movables can be pushed
            if (not movables or
                (movables and
                 self.level.sprite_can_enter(
                     movables[0]._get_dest_pos(direction)))):
                if movables:
                    self.pushing |= set(movables)
                self.start_move(direction)


    def do_move(self, elapsed):
        """Move the player and also move pushed sprites."""
        distance = Sprite.do_move(self, elapsed)

        for spr in self.pushing.copy():
            spr.pos = spr._get_dest_pos(self.move_dir, distance)
            if self.to_move == 0:
                self.pushing.discard(spr)

