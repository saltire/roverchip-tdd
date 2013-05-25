from pyg.window import Window
from pyg.gamescreen import GameScreen
from roverchip.leveldata.tiledmap import TiledMap


with open('levels/soko1.tmx', 'rb') as lfile:
    leveldata = TiledMap(lfile.read())

result = Window().run(GameScreen(leveldata))

print 'Yay!' if result else 'Ouch!'

