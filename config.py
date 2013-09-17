import os


path = lambda p: os.path.realpath(os.path.join(os.path.dirname(__file__), p))


# pygame general

keyrepeat = 100

# pygame window

windowsize = 800, 400
minsize = 200, 120
animation = True

# levels

levelpath = path('levels/*.tmx')

# menu

menubackcolor = 255, 255, 255
menufontcolor = 0, 0, 0
menuratio = 3, 2
menumargin = 0.05, 0.05
textmargin = 0.05, 0.1

menufontpath = path('pyg/font.png')
menufontsize = 8, 8

maxrows = 8
maxfontsize = 96
minfontsize = 8
sizestep = 8
columns = 2
leadpct = 0.4

# game

tilepath = path('pyg/tiles.png')
tilesize = 16, 16
maxviewcells = 20, 20
