"""pplsftlct - peoplesoft leave and compensatory time"""
path = r'C:\Users\USER\Desktop\info.txt'


import re
from time import strptime, strftime


FORMAT = '%Y-%m-%d'
# accepts ISO 8601, DD.MM.YYYY, MM/DD/YYYY dates
pattern = r'([\w]{3})[\w ]+\n[\w ]+\n\w+\n\d+[-./]\d+[-./]\d+\n([-\d.,]+)\n([\d.,]+)\n([\d.,]+)\n\t([-\d.,]+)\n(\d+[-./]\d+[-./]\d+)'

def sf(s): #convert special string to float
    hs = False # hit seperator
    o = ''
    for c in s:
        if c.isnumeric() or c == '-':
            o += c
        elif not hs and c in ['.', ',']:
            hs = True
            o += c
    return o

def sd(s):
    return strptime(s, FORMAT)

text = open(path).read()
matches = re.findall(pattern, text)
formats = [str, float, float, float, sf, sd]

od = {} # outputdict
for match in matches:
    match = list(match)
    if '.' in match[5]: # DD.MM.YYYY to ISO_8601
        match[5] = strptime(match[5], '%d.%m.%Y')
    elif '/' in match[5]: # MM/DD/YYYY to ISO_8601
        match[5] = strptime(match[5], '%m/%d/%Y')
    else:
        match[5] = strptime(match[5], FORMAT)
    match[4] = sf(match[4])
    for i in range(1,5):
        match[i] = match[i].replace('.', ',') # changes decimal seperator . to excel ,
    key = match[5]
    subkey = match[0]
    od[key] = {}
    od[key][subkey] = match[1:5]

headers = ['Accrual Date', 'Plan', 'Starting Balance', 'Units Earned', 'Units Taken', 'End Balance']
print("\t".join(headers))
for key, val in od.items():
    for sk, sv in val.items():
        print(strftime(FORMAT, key), sk, "\t".join(sv), sep="\t")
