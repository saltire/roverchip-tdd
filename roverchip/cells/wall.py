from cell import Cell


class Wall(Cell):
    def __init__(self):
        Cell.__init__(self)

        self.player_can_enter = False
        self.sprite_can_enter = False
