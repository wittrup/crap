import turtle
from amazon import Boa
from random import randrange
import threading

# from keysclass import Keys
# import configparser
import winsound


def controlthread(arg1, stop_event, fwd, rev, left, right):
    step = 5
    turnstep = 15
    while (not stop_event.is_set()):
        stop_event.wait(0.1)
        if left.is_set() and not right.is_set():
            player.left(turnstep)
        if right.is_set() and not left.is_set():
            player.right(turnstep)
        if fwd.is_set() and not rev.is_set():
            player.forward(step)
        if rev.is_set() and not fwd.is_set():
            player.backward(step)


def movethread(arg1, stop_event):
    while (not stop_event.is_set()):
        stop_event.wait(0.1)
        turtle.tracer(50)
        for bullet in bullets:
            if bullet.isvisible():
                bpos = bullet.pos()
                bullet.advance(75)
                for boa in boas:
                    if boa.collisionwith(37, bpos) or boa.collisionwith(37, bullet.pos()):
                        boa.hideturtle()
        for boa in boas:
            if boa.isvisible():
                boa.advance(20)
        turtle.title(str(len(bullets)) + ' ' + str(len(boas)))
        turtle.tracer(1)

def hitthread(arg1, stop_event):
    while (not stop_event.is_set()):
        stop_event.wait(0.9)
        victory = True
        for boa in boas:
            victory = victory and not boa.isvisible()
            if boa.isvisible() and boa.collisionwith(20, player.pos()):
                print('HIT!')
        if victory:
            print('memente mori')

def pewthread(arg1, stop_event, pew):
    while not stop_event.is_set():
        stop_event.wait(0.1)
        if pew.is_set():
            pew.clear()
            winsound.Beep(1000, 100)

def onspace():
    pew.set()
    turtle.tracer(50)
    bullet = Boa()
    bullet.collisionkill = True
    bullet.goto(player.pos())
    bullet.setheading(player.heading())
    bullets.append(bullet)
    turtle.tracer(1)

def okpUp():
    if not fwd.is_set():
        fwd.set()
def okrUp():
    fwd.clear()

def okpDown():
    if not rev.is_set():
        rev.set()
def okrDown():
    rev.clear()

def okpLeft():
    if not left.is_set():
        left.set()
def okrLeft():
    left.clear()

def okpRight():
    if not right.is_set():
        right.set()
def okrRight():
    right.clear()

turtle.tracer(50)
player = Boa()
player.appendline([-300,300], [300, 300]) # top
player.appendline([-300,-300], [300, -300]) # bottom
player.appendline([-300,300], [-300, -300]) # left
player.appendline([300,300], [300, -300]) # right
player.drawlines()
player.shape('turtle')
player.color('red')

boas = []
for i in range(1, 7):
    boas.append(Boa())
for boa in boas:
    boa.shape('circle')
    boa.lines = player.lines
    boa.collisionautoturn = True
    boa.setheading(randrange(360))
    boa.forward(200)

bullets = []

# config = configparser.ConfigParser()
# config.optionxform=str  # preserve case
# config.read('config.ini')
# keys = Keys(player, config)

winsound.Beep(32767, 0)

turtle.onkeypress(okpUp, 'Up')
turtle.onkeyrelease(okrUp, 'Up')

turtle.onkeypress(okpDown, 'Down')
turtle.onkeyrelease(okrDown, 'Down')

turtle.onkeypress(okpLeft, 'Left')
turtle.onkeyrelease(okrLeft, 'Left')

turtle.onkeypress(okpRight, 'Right')
turtle.onkeyrelease(okrRight, 'Right')

turtle.onkeypress(onspace, 'space')
print(player.lines)
thread_stop = threading.Event()

pew = threading.Event()
pt = threading.Thread(target=pewthread, args=(2, thread_stop, pew))
pt.daemon = True
pt.start()

fwd = threading.Event()
rev = threading.Event()
left = threading.Event()
right = threading.Event()
ct = threading.Thread(target=controlthread, args=(5, thread_stop, fwd, rev, left, right))
ct.daemon = True
ct.start()

t = threading.Thread(target=movethread, args=(1, thread_stop))
t.daemon = True
t.start()


h = threading.Thread(target=hitthread, args=(2, thread_stop))
h.daemon = True
h.start()



turtle.tracer(1)
turtle.listen()
turtle.mainloop()

thread_stop.set()