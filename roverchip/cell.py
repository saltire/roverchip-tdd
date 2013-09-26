class Cell:
    def __init__(self):
        self.type = self.__class__.__name__

        # defaults to override
        self.rotate = 0                 # rotation of the tile
        self.enemy_can_enter = True     # enemies can enter this cell
        self.player_can_enter = True    # player can enter this cell
        self.sprite_can_enter = True    # sprites can enter this cell
