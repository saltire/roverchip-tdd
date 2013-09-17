from pyg.window import Window
from pyg.gamescreen import GameScreen
from roverchip.leveldata.tiledmap import TiledMap


levelfiles = ['levels/soko1.tmx']
window = Window()

for levelfile in levelfiles:
    with open(levelfile, 'rb') as lfile:
        leveldata = TiledMap(lfile.read())
        result = window.run(GameScreen(leveldata))

print 'Yay!' if result else 'Ouch!'
