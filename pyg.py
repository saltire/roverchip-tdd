from pyg.window import Window
from pyg.gamescreen import GameScreen
from roverchip.test.test_level import MockDataFile


cells = [[0, 0, 0, 0],
         [0, 0, 0, 1],
         [0, 0, 0, 1]]
ctypes = [('Floor',), ('Grate',)]
sprites = [('Player', (1, 1)), ('Crate', (2, 1)), ('Crate', (2, 2))]
leveldata = MockDataFile(cells, ctypes, sprites, 'SokobanLevel')

result = Window().run(GameScreen(leveldata))

print 'Yay!' if result else 'Ouch!'

