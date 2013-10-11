from roverchip.cell import Cell
from roverchip.cells.mixins.button import Button


class ToggleButton(Button, Cell):
    def trigger(self, sprite):
        """Toggle the solidity of all toggle sprites."""
        for toggle in sprite.level.sprites['Toggle']:
            toggle.is_solid = not toggle.is_solid
