"""pplsftlct - peoplesoft leave and compensatory time"""
path = r'C:\Users\USER\Desktop\info.txt'


import re
from time import strptime, strftime


FORMAT = '%Y-%m-%d'# %H:%M:%S'
pattern = r'([\w]{3})[\w ]+\n[\w ]+\n\w+\n\d+-\d+-\d+\n([-\d.]+)\n([\d.]+)\n([\d.]+)\n\t([-\d.]+)\n(\d+-\d+-\d+)'
def sf(s): #convert special string to float
    hs = False # hit seperator
    o = ''
    for c in s:
        if c.isnumeric():
            o += c
        elif c == '-':
            o += c
        elif not hs and c == '.':
            hs = True
            o += c
    return o

def sd(s):
    return strptime(s, FORMAT)

text = open(path).read()
matches = re.findall(pattern, text)
headers = ['Plan', 'Starting Balance', 'Units Earned', 'Units Taken', 'End Balance', 'Accrual Date']
formats = [str, float, float, float, sf, sd]

print("\t".join(headers))
od = {} # outputdict
for match in matches:
    match = list(match)
    #for p, format in enumerate(formats):
    #    match[p] = format(match[p])
    match[5] = strptime(match[5], FORMAT)
    match[4] = sf(match[4])
    key = match[5]
    subkey = match[0]
    od[key] = {}
    od[key][subkey] = match[1:5]

for key, val in od.items():
    if key > strptime('2016-02-01', FORMAT):
        for sk, sv in val.items():
            print(strftime(FORMAT, key), sk, "\t".join(sv), sep="\t")
