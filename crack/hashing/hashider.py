import hashtest
import re
from passwdformats import FILE_FORMAT

file_format = 'custom'
methods = 'methods'
target = 'target.passwd'
usr = ''

hashlist = {}
pattern = r'([^#].*)(:)(.*)(:)(.*)(:)(.*)(:)(.*)(:)'
f = open(target)
for line in f:
    match = re.match(pattern, line, re.I | re.U)
    if hasattr(match, 'group'):
        uname = match.group(1)
        hashlist[uname] = dict(zip(FILE_FORMAT[file_format], match.groups()[::2]))


pwd = hashlist[usr]['pass']
slt = hashlist[usr]['salt']
answer = hashlist[usr]['hash']

f = open(methods)
winners = []
errors = []
misses = []
for line in f:
    if any(hash in line for hash in ['md5', 'sha1']):
        lirs = line.rstrip()
        result = hashtest.decode(lirs, usr, pwd, slt)
        if answer in result[0]:
            winners.append(result)
        elif 'Error' in result[2]:
            errors.append(result)
        else:
            misses .append(result)

for winner in winners:
    print(winner)

print("\n", '=' * 40, "\n")
for error in errors:
    print(error)

print("\n", '=' * 40, "\n")
for miss in misses:
    print(miss)
