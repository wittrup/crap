from definitions import whspchars
from lookups import instr_mod

f = open('helloworld.ws')
for line in f:
    wscmd = ''
    for c in line:
        wscmd += c if c in whspchars else ''
    # for c in wscmd:

    for c in whspchars:
        line = line.replace(c, '')
    print(line, repr(wscmd), instr_mod(wscmd))