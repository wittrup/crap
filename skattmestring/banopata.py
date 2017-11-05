#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PEP  263 -- Defining Python Source Code Encodings                         https://www.python.org/dev/peps/pep-0263/
# PEP 3120 -- Using UTF-8 as the default source encoding                    https://www.python.org/dev/peps/pep-3120/

"""
banopata - Banking Nordea Parse Transactions
"""

from common import *
import re


if __name__ == '__main__':
    PathToProperties = config["PathToProperties"]
    PathToTransactions = config["PathToTransactions"]

    errors = []
    for line in open(PathToTransactions, encoding='utf-8').readlines():
        fields = line.rstrip().split('\t')
        if len(fields) > 5 and all([fields[:2], fields[3], fields[5]]) and '.' in fields[0]:
            datebook, typetrns, text, datevald, accout, accoin = fields
            d, M, Y = map(int, datebook.split('.'))
            accoin = safe_cast(accoin.replace(',', '.').replace(' ', ''), float, .0)

            navn = re.findall(r"[\w']+", text.upper())
            navn = ' '.join((navn[0], navn[-1])) if len(navn) > 0 else ''
            keysearch = max(similar(navn, key) for key in unitlookup.keys())
            molike = keysearch[1]  # most likely key
            if molike in unitlookup and molike == navn and datebook == datevald:
                unit = unitlookup[molike]
                if not unit in data:
                    data[unit] = {}
                if not "payments" in data[unit]:
                    data[unit]["payments"] = {}
                if not Y in data[unit]["payments"]:
                    data[unit]["payments"][Y] = {}
                if not M in data[unit]["payments"][Y]:
                    data[unit]["payments"][Y][M] = {}
                data[unit]["payments"][Y][M][d] = accoin
            else:
                errors.append(str((fields, keysearch)))
savedata()

print('#' * 50, 'ERRORS', '#' * 50)
print('\n'.join(errors))
