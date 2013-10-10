from roverchip.sprite import Sprite
from roverchip.spritegroup import SpriteGroup


class Player(Sprite):
    priority = 1
    tile_rotates = True
    is_destructible = True

    def __init__(self, level, (x, y)):
        Sprite.__init__(self, level, (x, y))

        self.carrying = SpriteGroup()       # sprites carried by the player
        self.followers = SpriteGroup()      # sprites following the player
        self.pushing = SpriteGroup()        # sprites being pushed
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
        """Kill the player if it's touching any enemies.
        Start the player moving if stopped and key is down."""
        if self.level.sprites.enemy.on(self.pos):
            self.is_active = False
            return

        if (self.move_key_queue and not self.to_move and not self.delay_left):
            self.attempt_move(self.move_key_queue[0])


    def attempt_move(self, direction):
        """Start the player moving, and push movable objects."""
        self.rotate = direction

        nextpos = self.get_pos_in_dir(direction)

        for door in self.level.sprites['Door'].solid.on(nextpos):
            door.attempt_open(self)

        if self.level.player_can_enter(nextpos):
            movables = self.level.sprites.movable.at(nextpos)
            # proceed only if no movables or movables can be pushed
            if (not movables or self.level.sprite_can_enter(self.get_pos_in_dir(direction, 2))):
                self.pushing |= movables
                for item in self.pushing:
                    item.move_dir = direction
                self.start_move(direction)


    def start_move(self, direction):
        """Start followers moving as well."""
        Sprite.start_move(self, direction)
        # followers move toward player's previous location
        for follower in self.followers:
            follower.start_move(follower.get_dir_of_pos(self.pos))


    def do_move(self, elapsed):
        """Move carried and pushed items at the same time as the player."""
        Sprite.do_move(self, elapsed)
        for item in self.carrying:
            item.pos = self.pos
        for movable in self.pushing:
            movable.pos = self.get_pos_in_dir(self.move_dir)


    def after_move(self):
        """Pick up items in this cell, and start adjacent Rovers following."""
        for item in self.pushing:
            item.after_move()
        self.pushing.clear()

        for item in self.level.sprites.active.item.on(self.pos):
            if item not in self.carrying:
                self.carrying.add(item)

        for sprite in self.level.sprites.on(*[self.get_pos_in_dir(direction)
                                              for direction in range(4)]):
            if sprite.type == 'Rover' and sprite not in self.followers:
                self.followers.add(sprite)


    def end_turn(self):
        """Kill the player if it is overlapping any enemies."""
        if self.level.sprites.enemy.on(self.pos):
            self.is_active = False
