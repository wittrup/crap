import re
from passwdformats import FILE_FORMAT # FILE_FORMAT['smbpasswd'] = ['name', 'uid', 'LM_hash', 'NTLM_hash', 'Account Flags', 'Last Change Time']

file = 'target.passwd'
file_format = 'custom'

userlist = {}
pattern = r'(.*)(:)(.*)(:)(.*)(:)(.*)(:)(.*)(:)'
f = open(file)
for line in f:
    match = re.match(pattern, line)#, re.I | re.U)
    if hasattr(match, 'group'):
        print(match.groups())
        uname = match.group(1)
        userlist[uname] = dict(zip(FILE_FORMAT[file_format], match.groups()[::2]))

print('-'*50)
for key, value in userlist.items():
    print(key, value)
