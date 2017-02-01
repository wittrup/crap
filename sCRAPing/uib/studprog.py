import requests
from os.path import isfile, exists
import os
import pickle
import studprogparser
from urllib.parse import urlparse


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def loadorget(url, filename, reload=False):
    if reload or not isfile(filename):
        r = requests.get(url)
        pickle.dump(r, open(filename, 'wb'), pickle.HIGHEST_PROTOCOL)
    else:
        r = pickle.load(open(filename, 'rb'))
    return r

def getstudpage(url, fil):
    r = loadorget(url, fil)
    studpageparser = studprogparser.StudPageParser()
    studpageparser.feed(r.text)
    return studpageparser

if __name__ == '__main__':
    url = r'http://www.uib.no/studieprogram'
    mkdir(r'ignore')
    r = loadorget(url, r'ignore/studieprogram')

    parser = studprogparser.StudProgParser()
    parser.feed(r.text)

    n = 0
    out =open(r'output.tsv', 'w', encoding='UTF-8')
    print('cat', 'studie', 'url', 'studieplasser', 'poenggrenser', 'obligatorisk emner', sep='\t', file=out)
    for cat, list in parser.result.items():
        for items in list:
            url = r'http://www.uib.no' + items[-1]
            s = getstudpage(url, r'ignore/' + urlparse(url).path.split('/')[-1])
            h = s.heading()

            subject = s.data('subject')
            studata = s.data('uib-study-data')
            d = {'obligatorisk emne': []}
            if studata:
                for k, v in studata:
                    i = subject[k]
                    d[i] = d[i] + [v] if i in d else [v]

            print(cat, *items, h['studieplassar'], h['poenggrense'], d['obligatorisk emne'], sep='\t', file=out)

            if n > 10:
                break
            n += 1
