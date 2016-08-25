from faulhaber_const import commands as FMCC
fautmel=['GTYP', 'GSER', 'VER', 'GN', 'GCL', 'GRM', 'GKN', 'RM', 'KN', 'ANSW', 'NET', 'CST', 'CO', 'SO', 'TO', 'SAVE', 'BAUD', 'NODEADR', 'GNODEADR', 'GADV', 'EN', 'DI', 'GTIMEOUT', 'TIMEOUT', 'UPTIME', 'SADV']

from crcmod.predefined import mkCrcFun as mkCrcFunPre
from crcmod import mkCrcFun

crcfuncs = {}
crcnames = ['crc-8', 'crc-8-darc', 'crc-8-i-code', 'crc-8-itu', 'crc-8-maxim', 'crc-8-rohc', 'crc-8-wcdma']
for crc_name in crcnames:
    crcfuncs[crc_name] = mkCrcFunPre(crc_name)

crcfuncs['CRC-13-BBC'] = mkCrcFun(0x1CF5)

cmds = {}
for cmd in FMCC:
    cmds[cmd] = {}
    for crc_name, crc_func in crcfuncs.items():
        cmds[cmd][crc_name] = crc_func(bytes(cmd, 'ascii'))

crccount = {}
for crc_name in crcnames:
    crccount[crc_name] = [0] * 256
    for cmd,value in cmds.items():
        crccount[crc_name][value[crc_name]] += 1

from collections import Counter
import operator
stats = {}
for crc_name in crcnames:
    stats[crc_name] = len([item for item, count in Counter(crccount[crc_name]).items() if count > 1])
crcleast = min(stats.items(), key=operator.itemgetter(1))[0]
print(crcleast, stats[crcleast])

collisions = {}
for checksum,count in enumerate(crccount[crcleast]):
    if count > 1:
        collisions[checksum] = []
        for cmd, value in cmds.items():
                if value[crcleast] == checksum:
                    collisions[checksum].append(cmd)

fautmelcollisions = []
for chksum, cms in collisions.items():
    cnt = 0
    hit = []
    for c in cms:
        if c in fautmel:
            cnt += 1
            hit.append(c)
    if cnt > 0:
        fautmelcollisions.append([chksum, cnt, cms, hit])

print("\n".join(map(str, fautmelcollisions)))
