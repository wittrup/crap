"""amazon module is a jungle containing different plants and creatures,
for instance the boa which is a reptile like the turtle,
however it may not moved around freely and can be constricted,
hence boa constrictor"""
import turtle

from random import shuffle, randrange
from math import radians, cos, sin

def even(number):
    """:param number: to be checked
    :return: Bool - True if number is even, False otherwise (return number % 2 == 0)"""
    return number % 2 == 0

def conv(value, fromLow=0, fromHigh=0, toLow=0, toHigh=0, func=None):
    """Re-maps a number from one range to another. That is, a value of fromLow would get mapped to toLow, a value of fromHigh to toHigh, values in-between to values in-between, etc.

Does not constrain values to within the range, because out-of-range values are sometimes intended and useful. The constrain() function may be used either before or after this function, if limits to the ranges are desired.

Note that the "lower bounds" of either range may be larger or smaller than the "upper bounds" so the conv() function may be used to reverse a range of numbers, for example
y = conv(x, 1, 50, 50, 1)

The function also handles negative numbers well, so that this example
y = conv(x, 1, 50, 50, -100)
is also valid and works well.

:param value:    the number to map
:param fromLow:  the lower bound of the value's current range
:param fromHigh: the upper bound of the value's current range
:param toLow:    the lower bound of the value's target range
:param toHigh:   the upper bound of the value's target range
:param func:     function to be applied on result
:return:         The mapped value."""
    result = (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow
    if func is None:
        return result
    else:
        return func(result)

def walltocord(wall, magnification=1, peakwidth=1):
    """creates a list of start and end coordinates for each line to be drawn from string representation of a maze wall
    :param wall:          string representation of wall
    :param magnification: magnification applied to output coordinates
    :param peakwidth:     A couple of weeks ago, cannot remember what I was thinking here...
    :return:              list of [(startpos * magnification, end_pos  * magnification)]"""
    """decodes a horizontal maze line and creates a list of start and end position for each line to be drawn"""
    out = []
    rising_edge = False
    startpos = 0
    for i, c in enumerate(wall):
        if c in '+-|': # value is above threshold
            if not rising_edge:
                rising_edge = True
                startpos = i
        else:
            if rising_edge: # this is falling edge
                rising_edge = False
                if startpos < i - peakwidth: # signal is wider than peak limit
                    out += [(startpos * magnification, (i - peakwidth) * magnification)] # append to list
    # after loop check if complete signal is high, if so append
    if rising_edge and startpos <= i - peakwidth:
        out += [(startpos * magnification, i  * magnification)]
    return out

# def isVec2D(x):
#     iscorrectlist = False
#     if x is list and len(x) >= 2:
#         iscorrectlist = bool(type(x[0]) is float and type(x[1]) is float)
#     return x is turtle.Vec2D or iscorrectlist

def samesideofline(pos, dest, line):
    """checks if pos and dest is on the same side of line

    :param pos:  a pair/vector of numbers as a Vec2D (e.g. as returned by pos())
    :param dest: a pair/vector of numbers as a Vec2D (e.g. as returned by pos())
    :param line: a list of two pairs/vectors of numbers as two Vec2D
    :return:     a number that can be used as bool
                  0 = pos and dest is on each side of line
                  1 = pos and dest is left of line
                  2 = pos and dest is over line
                  4 = pos and dest is right of line
                  8 = pos and dest is under line
                 16 = pos and dest is outside of line, should be considered as True as movement is allowed"""
    xli = min(line[0][0], line[1][0])   # min of x line cord
    xla = max(line[0][0], line[1][0])   # max of x line cord
    yli = min(line[0][1], line[1][1])   # min of y line cord
    yla = max(line[0][1], line[1][1])   # max of y line cord

    xpi = min(pos[0], dest[0])          # min of x pos and dest
    xpa = max(pos[0], dest[0])          # max of x pos and dest
    ypi = min(pos[1], dest[1])          # min of y pos and dest
    ypa = max(pos[1], dest[1])          # max of y pos and dest

    # if xli < xpi < xla or xli < xpa < xla:
    #     result = ypa < yli or ypi > yla
    # elif yli < ypi < yla or yli > ypa > yla:
    #     result = xpa < xli or xpi > xla
    # else:
    #     result = True
    # return result
    if xli < xpi < xla or xli < xpa < xla:
        if ypa < yli: # pos and dest is under line
            result = 8
        elif ypi > yla: # pos and dest is over line
            result = 2
        else:
            result = 0
    elif yli < ypi < yla or yli > ypa > yla:
        if xpa < xli: # pos and dest is left of line
            result = 1
        elif xpi > xla: # pos and dest is right of line
            result = 4
        else:
            result = 0
    else: # pos and dest is outside of line
        result = 16
    return result

def getmazeheight(maze):
    """seriously?
    I am really not sure what to write here, is there anything unclear with the function name?
    Ok, fair enough
    :param maze: string representation of maze
    :return:     the height of the maze given string representation (return (len(maze.split('&#92;n')) - 3) / 2)"""
    return (len(maze.split('\n')) - 3) / 2

def getmazewidth(maze):
    """Again?!?
    :param maze: string representation of maze
    :return:     the width of the maze given string representation (return maze.split('&#92;n')[0].count('+') - 1)"""
    return maze.split('\n')[0].count('+') - 1

class Boa(turtle.Turtle):
    collidewithlines = True
    collisionautoturn = False
    collisionkill = False
    lines = list()
    maze = ''
    step = 5

    def __init__(self, name=None, color=None):
        """Initialize self.  See help(type(self)) for accurate signature.

        :param name: Set name str for this instance
        :param color: Set the pencolor and fillcolor.
        :return: None
        """
        # super(Boa, self).__init__(self)
        turtle.Turtle.__init__(self)
        if type(name) is str:
            self.name = name
        if type(color) is str:
            self.color(color)
        self.penup()

    def getlines(self):
        "return self.lines"
        return self.lines

    def setmaze(self, maze):
        self.maze = maze

    def makemaze(self, w = 16, h = 8):
        """set self.maze to string representation of random generated maze

        :param w: int
        :param h: int
        :return: None
        """
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
        hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]: continue
                if xx == x: hor[max(y, yy)][x] = "+  "
                if yy == y: ver[y][max(x, xx)] = "   "
                walk(xx, yy)

        walk(randrange(w), randrange(h))

        s = ""
        for (a, b) in zip(hor, ver):
            s += ''.join(a + ['\n'] + b + ['\n'])
        self.maze = s

    def appendline(self, xf, yf, xt=None, yt=None):
        """appends a line from one coordinate to another to the list self.lines

        :param xf: a number or a pair/vector of numbers
        :param yf: a number or a pair/vector of numbers
        :param xt: a number or None
        :param yt: a number or None
        If xt and yt is None, xf and yf must be a pair of coordinates or a Vec2D (e.g. as returned by pos()).
        :return: None
        """
        if xt is None and yt is None:
            self.lines.append([xf,yf])
        else:
            self.lines.append([[xf,yf],[xt,yt]])

    def drawline(self, fromcord, tocord):
        """Draws a line from :param fromcord to :param tocord
        :param fromcord: a pair of coordinates or a Vec2D (e.g. as returned by pos()).
        :param tocord: a pair of coordinates or a Vec2D (e.g. as returned by pos()).
        :return: None"""
        self.penup()
        self.goto(fromcord)
        self.pendown()
        self.goto(tocord)

    def drawlines(self, drawcolor=None):
        " Draw all self.lines, tracer needs to be set to 1 after this"
        self._tracer(50)
        pencolor = self.pencolor()
        startpos = self.position()
        if type(drawcolor) is str:
            self.pencolor(drawcolor)
        else:
            self.pencolor('black')
        for line in self.lines:
            self.drawline(line[0], line[1])
        self.penup()
        self.pencolor(pencolor)
        self.setpos(startpos)

    def onkeypress(self, fun, key=None):
        """redirect to turtle.onkeypress()

In order to be able to register key-events, TurtleScreen
must have focus. (See method listen.)

:param fun: a function with no arguments
:param key: a string: key (e.g. "a") or key-symbol (e.g. "space")
:return: None
        """
        turtle.onkeypress(fun, key)

    def collisionwith(self, radius, x, y=None):
        """Returns if self.pos() is within radius of x, y

        :param radius: a number (integer or float)
        :param x: a number or a pair/vector of numbers
        :param y: a number or None
                  If y is None, x must be a pair of coordinates or a Vec2D (e.g. as returned by pos()).
        :return: Bool - True or False (return (cx - sx)**2 + (cy - sy)**2 < radius**2)"""
        if y is None:
            collider = x
        else:
            collider = [x,y]
        sx = self.pos()[0] # self pos x
        sy = self.pos()[1] # self pos y
        cx = collider[0] # collider x
        cy = collider[1] # collider y
        return (cx - sx)**2 + (cy - sy)**2 < radius**2

    def loadmazeintolines(self, maze, zero):
        """
        :param maze: string representation of the maze to be loaded into self.lines
        :param zero: dict containg 'left', 'right', 'top' and 'bottom' zero offest
        :return: None
        """

        mazewidth = getmazewidth(maze)
        mazeheight = getmazeheight(maze)
        screenwidth = abs(zero['left'] - zero['right'])
        screenheight = abs(zero['top'] - zero['bottom'])
        y = 0
        # handle vertical lines
        for i,wall in enumerate(maze.split('\n')):
            if even(i):
                ycord = conv(y, in_max=mazeheight, out_min=zero['top'], out_max=zero['bottom'])
                for line in walltocord(wall, screenwidth / mazewidth / 3):
                    xfrom = line[0] + zero['left']
                    xdest = line[1] + zero['left']
                    self.appendline([xfrom, ycord], [xdest, ycord])
                y += 1
        # handle horizontal lines
        for x in range(0, mazewidth + 1):
            wall = ''
            for i,c in enumerate(maze[3 * x::50]):
                wall += c
            xcord = conv(x, in_max=mazewidth, out_min=zero['left'], out_max=zero['right'])
            for line in walltocord(wall, screenheight / mazeheight / 2):
                yfrom = zero['top'] - line[0]
                ydest = zero['top'] - line[1]
                self.appendline([xcord, yfrom], [xcord, ydest])

    def advance(self, distance):
        """Move the boa forward() by the specified distance if allowed (not crossing any lines unless allowed to, hiding on collision and bouncing if set to)

        :param distance: a number (integer or float)
        :return: None"""
        self.movedir(distance)

    def reverse(self, distance):
        """Move the boa forward() by the specified distance if allowed (not crossing any lines unless allowed to, hiding on collision and bouncing if set to)

        :param distance: a number (integer or float)
        :return: None"""
        self.movedir(distance * -1)

    def movedir(self, distance):
        """moves a given distance if allowed
        similar to turtle.forward() and turtle.backward()
        positive number moves forward
        negative number moves backward

        :param distance: int
        :return: None
        """
        dest = list(self.pos())
        bearing = self.heading()
        angle = 90 - bearing
        dest =[dest[0] + (distance * cos(radians(bearing))), dest[1] + (distance * cos(radians(angle)))]
        self.gotoifallowed(dest)

    def gotoifallowed(self, x, y=None):
        """goto() if allowed (not crossing any lines unless allowed to, hiding on collision and bouncing if set to)

        :param x: a number or a pair/vector of numbers
        :param y: a number or None
                  If y is None, x must be a pair of coordinates or a Vec2D (e.g. as returned by pos()).
        :return: None"""
        pos = self.pos()
        if y is None:
            dest = x
        else:
            dest = [x,y]

        premission = True
        for line in self.lines:
            premission = premission and samesideofline(pos, dest, line)
            if not premission:
                break
        if premission or not self.collidewithlines:
            self.goto(x, y)
        elif self.collisionkill: # on collision kill self instance class
            self.hideturtle()
            #del self
        elif self.collisionautoturn:
            sideofline = samesideofline(pos, pos, line) # left = 1, 2 = up, 4 = right, 8 = down
            newheading = randrange(180)
            if sideofline == 1:
                newheading += 90
            elif sideofline == 4:
                newheading -= 90
            elif sideofline == 8:
                newheading += 180
            self.setheading(newheading)

            dest = list(self.pos())
            bearing = self.heading()
            angle = 90 - bearing
            dest =[dest[0] + (self.step * cos(radians(bearing))), dest[1] + (self.step * cos(radians(angle)))]
            self.gotoifallowed(dest)


def testmaze():
    """:return: String representation of maze used for testing.
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                       |                    |  |
+  +--+--+--+--+--+--+  +  +--+--+--+--+--+  +  +
|  |           |     |  |           |     |     |
+  +--+--+  +  +  +--+  +--+--+--+  +--+  +--+  +
|           |  |     |           |     |     |  |
+--+--+--+--+  +--+  +--+--+--+  +  +--+--+  +  +
|           |     |     |        |        |  |  |
+--+--+--+  +--+  +--+  +  +--+--+--+  +--+  +  +
|              |     |  |           |        |  |
+  +--+--+  +--+--+  +  +--+--+--+  +--+--+--+  +
|  |     |  |        |           |     |        |
+  +  +  +--+  +--+--+--+--+  +--+  +--+  +--+--+
|     |     |  |           |  |     |     |     |
+  +--+--+  +  +--+  +--+  +  +  +--+  +--+--+  +
|        |           |        |                 |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

"""
    maze = \
"""+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|                       |                    |  |
+  +--+--+--+--+--+--+  +  +--+--+--+--+--+  +  +
|  |           |     |  |           |     |     |
+  +--+--+  +  +  +--+  +--+--+--+  +--+  +--+  +
|           |  |     |           |     |     |  |
+--+--+--+--+  +--+  +--+--+--+  +  +--+--+  +  +
|           |     |     |        |        |  |  |
+--+--+--+  +--+  +--+  +  +--+--+--+  +--+  +  +
|              |     |  |           |        |  |
+  +--+--+  +--+--+  +  +--+--+--+  +--+--+--+  +
|  |     |  |        |           |     |        |
+  +  +  +--+  +--+--+--+--+  +--+  +--+  +--+--+
|     |     |  |           |  |     |     |     |
+  +--+--+  +  +--+  +--+  +  +  +--+  +--+--+  +
|        |           |        |                 |
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

"""
    return maze