import impat
impat.addfolder('python')
from FunCom import find_between
from session import login, host, cookies
import requests

page=find_between(login.text, "top.location='/", "';")

if login.status_code == requests.codes.ok and cookies['SESSION'] is not '':
    print('=~=~=~=~=~=~=~=~=~=~=~=                               =~=~=~=~=~=~=~=~=~=~=~=')
    f = requests.get('http://%s/%s' % (host, page), cookies=login.cookies)
    print(f.text)