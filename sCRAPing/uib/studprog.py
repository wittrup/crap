import requests
from os.path import isfile, exists
import os
import pickle
import studprogparser


url = r'http://www.uib.no/studieprogram'

def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

mkdir(r'ignore')
if isfile(r'ignore/studieprogram'):
    r = pickle.load(open(r'ignore/studieprogram', 'rb'))
else:
    r = requests.get(url)
    pickle.dump(r, open(r'ignore/studieprogram', 'wb'), pickle.HIGHEST_PROTOCOL)

parser = studprogparser.StudProgParser()
parser.feed(r.text)

for cat, list in parser.result.items():
    for items in list:
        print(cat, *items, sep='\t')