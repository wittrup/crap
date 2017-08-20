import requests
import PyPDF2
from urllib.parse import urlsplit, parse_qsl
from os.path import isfile
import os
from time import sleep
from random import randrange


def _mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download(knr, gnr, bnr, fnr, snr, sfx='', filename='ignore/'):
    url = r'https://norgeskart.no/ws/grunnbok.py?knr=%s&gnr=%s&bnr=%s&fnr=%s&snr=%s&download=true' % (knr, gnr, bnr, fnr, snr)

    d = dict(parse_qsl(urlsplit(url).query))
    filename += '/' if not filename[-1] == '/' else ''
    _mkdir(filename)
    for i, key in enumerate(['knr', 'gnr', 'bnr', 'fnr', 'snr']):
        filename += d[key].rjust(4, '0') + (' ' if i < 4 else '')
    if sfx:
        filename += ' ' + sfx
    filename += '.pdf'

    if not isfile(filename):
        print('Fetching', url)
        r = requests.get(url)
        sleep(randrange(756, 3245)/1000)
        with open(filename, 'wb') as f:
            f.write(r.content)
    return filename

def pdfextracttext(filename):
    pdfFileObj = open(filename,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    text = ''
    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        text += pageObj.extractText()
    pdfFileObj.close()
    return text

if __name__ == '__main__':
    knr, gnr, bnr, fnr, snr = [l.strip() for l in open("ignore/gbtest.txt", encoding='utf-8').readlines()]

    fnm = download(knr, gnr, bnr, fnr, snr)
    txt = pdfextracttext(fnm)
    start, stop = False, False
    for line in txt.split('\n'):
        if line.upper() in ['HJEMMELSOPPLYSNINGER']:
            start = True
        if line.upper() in ['HEFTELSER']:
            stop = True
        if not stop and start:
            print(line)
