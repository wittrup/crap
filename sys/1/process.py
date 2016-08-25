from glob import iglob
from sys_1 import Parser
from os.path import isfile

o = open('ignore/output.txt', 'w', encoding='utf-8')
i=0
for fname in iglob('ignore/**/*.html', recursive=True):
    i+=1
    if isfile(fname):
        parse = Parser()
        for chunk in open(fname, encoding='utf-8'):
            parse.feed(chunk)
        print(parse.data, file= o)
print(i)
