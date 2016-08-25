from urllib.parse import urlparse
import os.path
import requests
from time import sleep
from random import randrange
import glob
import parsers
import time
import csv
import cleaner


AD_URL = 'http://m.finn.no/job/fulltime/ad.html?finnkode='
update = ['sqamlr1dlesu0qiarus6pvzjgh']

listdict = {}
for line in open('lists.txt'):
    url = line.rstrip()
    if not url.startswith('#'):
        query = urlparse(url)[4].split('=')
        share = query[1]
        fname = 'favorites/' + share + '.html'
        listdict[share] = fname

        if not os.path.isfile(fname) or share in update:
            # if file not exists, request file, save and wait for next
            print('Fetching', url, 'to', fname)
            r = requests.get(url)
            print(r.text, file=open(fname, 'w'))
            sleep(randrange(1500, 3500) / 1000)


parser = parsers.ListParser()
for key, fname in listdict.items():
    for chunk in open(fname):
        parser.feed(chunk)


# If ad file not in ads fetch files
titles = {}
adsdict = {}
for key, val in parser:
    titles[key] = val
    url = AD_URL + str(key)
    fname = 'ads/' + str(key) + '.html'
    adsdict[key] = fname
    if not os.path.isfile(fname):
        print('Fetching', url, 'to', fname)
        r = requests.get(url)
        print(r.text, file=open(fname, 'w'))
        sleep(randrange(1500, 3500) / 1000)

print(titles)

jobdict = {}
for key, fname in adsdict.items():
    key = int(os.path.basename(fname).split('.')[0])
    adparser = parsers.AdParser()
    for chunk in open(fname):
        adparser.feed(chunk)
    adparser.clean()

    jobdict[key] = adparser

print(jobdict)


header = ['id', 'title', 'arbeidsgiver', 'frist', 'tiltredelse', 'varighet', 'sektor', 'sted']
if header is None:
    for key, val in jobdict.items():
        for sk in val:
            if sk not in header:
                header.append(sk)
    print(header)

jobfile = open('jobs.txt', 'w', encoding='utf-8')
line = ''
for h in header:
    line += '\t' + h
print(line[1:], file=jobfile)


for key, val in jobdict.items():
    print(key, end='', file=jobfile)
    line = ''
    for h in header:
        if h == 'title':
            p = titles[key][h]
        elif h in ['frist', 'tiltredelse']:
            try:
                p = time.strftime('%Y-%m-%d', time.strptime(val[h], "%d.%m.%Y"))
                # p = datetime.datetime.strptime(val[h], "%d.%m.%Y")
            except:
                p = 'ASAP'
        elif h in ['arbeidsgiver'] and h in val:
            p = cleaner.uniquewords(val[h], True)
        elif h in val:
            p = val[h]
        else:
            p = ''
        line += '\t' + p
    print(line[1:], file=jobfile)
        # sv = val[sk]
        # print(sk, sv)