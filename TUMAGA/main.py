import turtle
from amazon import Boa
from keysclass import Keys
import configparser

screensizemin = min(turtle.screensize())
zero = {'left': screensizemin * -1}
zero['right'] = screensizemin
zero['top'] = screensizemin
zero['bottom'] = screensizemin * -1

def setcmd1():
    keys.settargetboa(a)
def setcmd2():
    keys.settargetboa(b)
def setcmd3():
    keys.settargetboa(c)
def setcmd4():
    keys.settargetboa(d)

if __name__ == '__main__':
    turtle.tracer(50)
    a = Boa('Leonardo', 'blue')
    b = Boa('Michelangelo', 'orange')
    c = Boa('Raphael', 'red')
    d = Boa('Donatello', 'purple')
    boas = [a, b, c, d]

    a.makemaze()
    # a.loadmaze(boa.testmaze())
    for boa in boas:
        boa.shape('turtle')
        boa.loadmazeintolines(a.maze, zero)
        boa.goto(10, 10)
    a.drawlines()
    turtle.tracer(1)

    config = configparser.ConfigParser()
    config.optionxform=str  # preserve case
    config.read('config.ini')
    keys = Keys(a, config)

    turtle.onkeypress(setcmd1, '1')
    turtle.onkeypress(setcmd2, '2')
    turtle.onkeypress(setcmd3, '3')
    turtle.onkeypress(setcmd4, '4')


    turtle.listen()
    turtle.mainloop()