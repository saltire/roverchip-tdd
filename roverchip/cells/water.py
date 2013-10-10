from roverchip.cell import Cell


class Water(Cell):
    player_can_enter = False
    enemy_can_enter = False

    def __init__(self, flow_dir=None):
        Cell.__init__(self)

        self.flow_dir = flow_dir
