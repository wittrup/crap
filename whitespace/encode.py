def num_to_ws(num, fmt=None, space=" ", tab="\t"):
    if fmt == None:
        fmt = "{0:08b}"
    return fmt.format(num).replace('0', space).replace('1', tab)

def line_to_ws(line):
    s = ''
    for c in line:
        s += "S S S S "
        s += num_to_ws(ord(c), None, "S ", "T\t")
        s += "L" + chr(10) + "T\tL" + chr(10)

    return s

def stripws(line):
    return line.replace(chr(10), 'N').replace("\t", 'T').replace(" ", "_")

f = open('expected_output.txt')
your_output = open('Your Output.txt', 'w')

for line in f:
    print(stripws(line), '#'*5, line_to_ws(line), sep='', end='', file=your_output)
    # print(line_to_ws(chr(10)), sep='', end='')
print("S S L"+chr(10)+"L"+chr(10), end='', file=your_output) # End of program
print("Done!")