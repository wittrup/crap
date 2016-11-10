import impat
impat.addfolder('python')
from random import randrange
from FunCom import find_between
from session import login, host, usr, pwd
import requests

print(login)
print(login.cookies)

if login.status_code == requests.codes.ok:
    print('=~=~=~=~=~=~=~=~=~=~=~=                               =~=~=~=~=~=~=~=~=~=~=~=')
