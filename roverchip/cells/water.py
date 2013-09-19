from cell import Cell


class Water(Cell):
    def __init__(self, flow_dir=None):
        Cell.__init__(self)

        self.player_can_enter = False
        self.robot_can_enter = False

        self.flow_dir = flow_dir
