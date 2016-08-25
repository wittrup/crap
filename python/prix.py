"""prix polynomial reversed init-value xor-out finder"""
from crcmod import mkCrcFun
from faulhaber_const import commands
import time

match = open('prix.txt', 'w+')
start = time.clock()
lastpos = 0
for possibility in range(0x2000000):
    polynomial = (possibility & 0xff) | 0x100
    init_value = (possibility & 0xff00) >> 8
    xor_output = (possibility & 0xff0000) >> 16
    revers = bool(possibility & 0x1000000) >> 17
    crcunction = mkCrcFun(polynomial, init_value, revers, xor_output)

    collist = [False] * 0x100
    collision = False
    for cmd in commands:
        crc = crcunction( bytes(cmd, 'ascii'))
        if collist[crc]:
            collision = True
            break
        collist[crc] = True
    if not collision:
        print('crc-8', possibility, 'WORKS' * 3, file=match)

    if time.clock() > start + 1:
        progress = possibility - lastpos
        lastpos = possibility
        print(progress, 'pr second')
        start = time.clock()
