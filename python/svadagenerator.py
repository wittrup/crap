import sys
import csv
from random import choice
from urllib.parse import quote_plus as quote
from difflib import SequenceMatcher

svada = {}
with open('svadagenerator.csv', 'r', encoding='utf-8') as csvfile:
    svadareader = csv.reader(csvfile, delimiter=';', quotechar="'")
    key = None
    for row in svadareader:
        if '' in row:
            key = row[0] if row[0] is not '' else None
            if key is not None:
                svada[key] = []
        elif key is not None:
            svada[key].append(row)

def similar(a, b):
    subst = a.lower() in b.lower() or b.lower() in a.lower()
    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio * (subst + 0.5), a, b

if len(sys.argv) > 1:
    arg = sys.argv[1]
    key = max(similar(key, arg) for key in svada.keys())[1]
else:
    key = choice(list(svada.keys()))

print('"*', ' '.join(choice(svada[key])), '*" - http://www.svadagenerator.no/?type=%s' % quote(key), sep='')
