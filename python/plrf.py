def csc(rawstr): #check sum control
    checksum = ord(rawstr[0])
    for char in rawstr[1:-2]:
        checksum += ord(char)
    return hex(checksum & 0xFF)[2:] == rawstr[-2:].lower()


def r2v(rawstr):
    stchr = rawstr[0]
    value = rawstr[1:-2]
    if stchr in ['d', 'a', 'e']:
        value = int(value) * 0.1

    if stchr is 'd':
        value = value * 0.1
    elif stchr is 'e' and value > 3141.5:
        value = value - 6283.2
    return (stchr, value)


if __name__ == '__main__':
    pattern = '(\w)(\d{2}[\dE]\d{3})([0-9A-Fa-f]{2})'
    examples = ['d00575095', 'a03825699', 'e0614569B', 'R00E3018B', 'a04372495', 'e06204495', 'd01010086', 'C00E21782', 'C00E21782']

    for rawstr in examples:
        print(csc(rawstr), rawstr, r2v(rawstr))
