#!/usr/bin/env python
# -*- coding: utf-8 -*-

from json import load, dump
from os import path
from difflib import SequenceMatcher


def jsloifex(filename):  # JSON load if exists
    return load(open(filename, encoding='utf-8')) if path.exists(filename) else {}

def savedata():
    dump(data, open(config["PathToData"], 'w', encoding='utf-8'), indent=2)
    print('Save data done')

def similar(a, b):
    subst = a.lower() in b.lower() or b.lower() in a.lower()
    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio * (subst + 0.5), a, b

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

config = jsloifex(r'ignore/config.json')
data = jsloifex(config["PathToData"])
unitlookup = jsloifex(config["PathToUnitLookup"])
