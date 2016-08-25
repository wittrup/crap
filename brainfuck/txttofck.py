"""loads text from
file - and prints a character map into
fcot - and prints commands into
fout - for ++ptr; or --ptr; and putchar(*ptr); through character map

Sounds greek?  Yes it is brainfucked!
"""

file = open('text.txt')
fcot = open('charmap.bf', 'w')
fout = open('your output.txt.bf', 'w')


####################################################################
chars = []
for line in file:
    for c in line:
        num = ord(c)
        if num not in chars:
            chars.append(num)
chars.sort()
ll = len(chars)

for i, t in enumerate(chars):
    x = chars[i - 1] if i > 0 else 0
    print('+' * (t - x), '[-', '>+' * (ll - i), '<' * (ll - i), ']', sep='', file=fcot)

chars.sort(reverse=True)
print(chars, file=fcot)

file.seek(0)
i = 0
print('> ', end='', file=fout)
for line in file:
    for c in line:
        idx = chars.index(ord(c))
        if idx > i:
            print('>' * (idx - i), '.', sep='', end=' ', file=fout)
        elif idx < i:
            print('<' * (i - idx), '.', sep='', end=' ', file=fout)
        else:
            print('.', sep='', end=' ', file=fout)
        if c == "\n":
            print('#', file=fout)
        i = idx
