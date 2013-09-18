from cell import Cell


class Grate(Cell):
    def __init__(self):
        Cell.__init__(self)

        self.robot_can_enter = False
