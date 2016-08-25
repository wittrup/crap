import requests
import re
from os.path import isfile
from time import sleep
from time import strftime as now
from random import shuffle, randrange


FORMAT = '%Y-%m-%d %H:%M:%S'
def log(data, file='fetch.log'):
    with open(file, 'a+') as f:
        f.write(now(FORMAT) + ' ' + str(data) + '\n')
        f.close()


if input('Are you sure? ') != 'YES':
    exit()
m = [l.strip() for l in open("../ignore/sys_1_misc.txt").readlines()]
details = {"username": m[1], "password": m[2]}
login = requests.Session()
login = login.post(m[0], data=details)

bids = list(range(1, int(m[3])+1))
shuffle(bids)

for i in bids:
    url = m[4] + str(i) + m[5]
    fname = 'b/' + str(i) + '.html'
    if not isfile(fname):
        log('Fetching %s' % (fname))
        r = requests.get(url, cookies=login.cookies)
        print(r.text, file=open(fname, 'w', encoding='utf-8'))
        sleep(randrange(1337, 1719) / 1000)
