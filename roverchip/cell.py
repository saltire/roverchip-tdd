class Cell:
    # default properties to override
    enemy_can_enter = True      # enemies can enter this cell
    player_can_enter = True     # player can enter this cell
    sprite_can_enter = True     # sprites can enter this cell

    def __init__(self):
        self.type = self.__class__.__name__

        # initial values
        self.rotate = 0         # rotation of the tile
