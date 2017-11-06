#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data To Payments Table
"""

from common import *


year = "2017"

Y = year
months = []
dates = {}  # OrderedDict() ?
for unit, fields in data.items():
    if "payments" in fields:
        for M, V in fields["payments"][year].items():
            M = int(M) if M.isnumeric() else 0
            if M not in months:
                months.append(M)
            if M not in dates:
                dates[M] = []
            for D in V:
                D = int(D) if D.isnumeric() else 0
                if D not in dates[M]:
                    dates[M].append(D)
            dates[M].sort(reverse=True)
months.sort(reverse=True)

print('enhet\tnavn', end='\t')
for m,ds in dates.items():
    for d in ds:
        print(str(d) + '.' + str(m), end='\t')
print('')

for k, v in data.items():
    payments = ''
    for m, ds in dates.items():
        m = str(m)
        if 'payments' in v and m in v['payments'][Y]:
            for d in ds:
                d = str(d)
                payments += str(int(v['payments'][Y][m][d])) + '\t' if d in v['payments'][Y][m] else '\t'
    if not payments:
        payments = 'EMPTY'
    print(k, v['eierekort'], payments, sep='\t')
