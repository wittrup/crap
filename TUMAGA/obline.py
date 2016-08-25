"oblique line"
__author__ = 'wittr'

from amazon import Boa
from keysclass import Keys
import configparser
import turtle

def samesideofline(pos, dest, line):
    "check if pos and dest is on same side of line, list of two Vec2D(x, y)"

    pass

player = Boa()



player.appendline(-100,0, 0, 100)
# player.appendline(0, 100, 100, 0)
player.drawlines()
player.collidewithlines = False

config = configparser.ConfigParser()
config.optionxform=str  # preserve case
config.read('config.ini')
keys = Keys(player, config)


turtle.tracer(1)
turtle.listen()
turtle.mainloop()