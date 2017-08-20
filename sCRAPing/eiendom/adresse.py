import requests
import json
from distutils.util import strtobool

from os.path import isfile, splitext as pathsplitext
import pickle
import collections
import grunnbok
import re


gatenavn, destfolder, husnrlav = [l.strip() for l in open("ignore/config.txt", encoding='utf-8').readlines()]
print('Lagrer grunnbøker for', gatenavn, 'i', destfolder)
husnrlav = int(husnrlav)

def loadorget(fetcher, url, filename, reload=False):
    if reload or not isfile(filename):
        r = fetcher(url)
        pickle.dump(r, open(filename, 'wb'), pickle.HIGHEST_PROTOCOL)
    else:
        r = pickle.load(open(filename, 'rb'))
    return r


if not isfile(r'ignore/Adresse'):
    url = r'http://ws.geonorge.no/AdresseWS/adresse/sok?sokestreng=%s&antPerSide=50' % gatenavn
    r = loadorget(requests.get, url, r'ignore/Adresse')
    assert r, 'Could not fetch data from geonorge'
    data = r.text
else:
    data = ''

adresser = loadorget(json.loads, data, r'ignore/Adresse.json')
assert adresser['totaltAntallTreff'].isnumeric(), "'totaltAntallTreff' is not numeric"
adresser['totaltAntallTreff'] = int(adresser['totaltAntallTreff'])
adresser['sokStatus']['ok'] = strtobool(adresser['sokStatus']['ok'])

if adresser['sokStatus']['ok'] and adresser['totaltAntallTreff'] > 0:
    unsdic = {} # unsorted dictionary
    for i, adresse in enumerate(adresser['adresser']):
        if type(adresse) is dict and adresse['husnr'].isnumeric():
            adresse['husnr'] = int(adresse['husnr'])
            if adresse['adressenavn'].lower() == gatenavn.lower() and adresse['husnr'] > husnrlav:
                bnr = adresse['bruksnr']
                if bnr not in unsdic:
                    unsdic[bnr] = {}
                hnr = str(adresse['husnr']) + (adresse['bokstav'] if 'bokstav' in adresse else '')
                if hnr not in unsdic[bnr]:
                    unsdic[bnr][hnr] = {}
                for k in ['kommunenr', 'gardsnr', 'festenr']:
                    unsdic[bnr][hnr][k] = adresse[k]
    od = collections.OrderedDict(sorted(unsdic.items()))
    for k, v in od.items():
        od[k] = collections.OrderedDict(sorted(v.items()))
        for sk, sv in od[k].items():
            od[k][sk] = collections.OrderedDict(sorted(sv.items()))
    liste = open(destfolder + '/' + 'oversikt.txt', 'w')
    for bruksnr, v in od.items():
        sns = 1 if len(v) > 1 else 0  # siste seksjonsnr
        for husnr, sv in v.items():
            filename = grunnbok.download(sv['kommunenr'], sv['gardsnr'], bruksnr, sv['festenr'], sns, husnr, destfolder)
            print(filename)
            text = grunnbok.pdfextracttext(filename)
            eiere = ''
            for match in re.findall(r'\n([\wÆØÅ]+) ([-\w ÆØÅ]+?)\s?(IDEELL:)? ?([\d/]*)\nF.NR: (\d+)', text):
                envn, fnvn, idel, andl, fnmr = list(match)
                fnvn = fnvn.split(' ')[0].split('-')[0].rstrip()
                if envn in eiere:
                    eiere = eiere.replace(' &', ',')
                    eiere = eiere.replace(' ' + envn, ' & ' + fnvn + ' ' + envn)
                else:
                    eiere += (' & ' if eiere else '') + fnvn + ' ' + envn
            print(husnr, eiere, file=liste, sep='\t')
            sns += 1
