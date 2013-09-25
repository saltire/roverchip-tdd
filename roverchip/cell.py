class Cell:
    def __init__(self):

        # defaults to override
        self.rotate = 0                 # rotation of the tile
        self.enemy_can_enter = True     # enemies can enter this cell
        self.player_can_enter = True    # player can enter this cell
        self.sprite_can_enter = True    # sprites can enter this cell


    def get_type(self):
        """Return the type of the cell, i.e. the class name."""
        return self.__class__.__name__
