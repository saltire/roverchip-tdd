from led.led import LED
from roverchip.leveldata.tiledmap import TiledMap


levelfiles = ['levels/soko1.tmx']
led = LED((32, 16))

for levelfile in levelfiles:
    with open(levelfile, 'rb') as lfile:
        leveldata = TiledMap(lfile.read())
        result = led.run_level(leveldata)
