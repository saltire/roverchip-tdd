import glob

import config
from pyg.window import Window
from pyg.menuscreen import MainMenuScreen
from roverchip.leveldata.tiledmap import TiledMap


window = Window()

leveldata = []
for levelfile in glob.glob(config.levelpath):
    with open(levelfile, 'rb') as lfile:
        leveldata.append(TiledMap(lfile.read()))

result = window.run(MainMenuScreen(leveldata))
