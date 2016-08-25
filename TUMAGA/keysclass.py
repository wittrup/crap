__author__ = 'wittr'

from math import radians, cos, sin

class Keys():

    def moveup(self):
        dest = list(self.boa.pos())
        dest[1] += self.step
        self.boa.setheading(90)
        self.boa.gotoifallowed(dest)

    def movedown(self):
        dest = list(self.boa.pos())
        dest[1] -= self.step
        self.boa.setheading(270)
        self.boa.gotoifallowed(dest)

    def strafeleft(self):
        dest = list(self.boa.pos())
        dest[0] -= self.step
        self.boa.setheading(180)
        self.boa.gotoifallowed(dest)

    def straferight(self):
        dest = list(self.boa.pos())
        dest[0] += self.step
        self.boa.setheading(0)
        self.boa.gotoifallowed(dest)

    def forward(self):
        self.boa.advance(self.step)

    def reverse(self):
        self.boa.reverse(self.step)

    def turnleft(self):
        self.boa.left(self.step)

    def turnright(self):
        self.boa.right(self.step)

    def _loadconfig(self, config):
        for section in config.sections():
            if section.lower() == 'keys':
                for key in config[section]:
                    name = config['Keys'][key]
                    if hasattr(self, name):
                        func = getattr(self, name) # a function with no arguments or None
                        self.boa.onkeypress(func, key)
                    else:
                        print(self, 'has no', name)


    def __init__(self, targetboa, config=None, step=5):
        self.boa = targetboa
        self.step = 5
        if config != None:
            self._loadconfig(config)

    def settargetboa(self, targetboa):
        self.boa = targetboa