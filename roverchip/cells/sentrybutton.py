from roverchip.cell import Cell
from roverchip.cells.mixins.button import Button


class SentryButton(Button, Cell):
    def trigger(self, sprite):
        """Cause all sentries to turn 180 degrees, which should start them moving."""
        for sentry in sprite.level.sprites['Sentry']:
            sentry.rotate = (sentry.rotate + 2) % 4
