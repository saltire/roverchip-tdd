from roverchip.cell import Cell


class Grate(Cell):
    def __init__(self):
        Cell.__init__(self)

        self.enemy_can_enter = False
