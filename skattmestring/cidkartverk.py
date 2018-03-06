#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cid - Copy Into Data Kartverk
"""

from common import *


if __name__ == '__main__':
    PathToData = config["PathToData"]
    PathToUnitLookup = config["PathToUnitLookup"]
    PathToProperties = config["PathToProperties"]


    for line in open(PathToProperties).readlines():
        enhet, eierekort, eierefull = line.rstrip().split('\t')
        for e in eierefull.split(', '):
            unitlookup[e] = enhet
        if not enhet in data:
            data[enhet] = {}
        data[enhet]['eierekort'] = eierekort
        data[enhet]['eierefull'] = eierefull

    dump(unitlookup, open(config["PathToUnitLookup"], 'w', encoding='utf-8'), indent=2)
# TODO:
#    make hash function of data, and check if this exists, if not store to some rollback file
    savedata()
