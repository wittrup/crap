import impat
impat.addfolder('python')
import requests
from FunCom import find_between
from session import host, cookies

f = requests.get('http://%s/pages/connectionStatus/content/status.html' % host, cookies=cookies)
print(find_between(f.text, "timeNow = '","';"))
print(find_between(f.text, "SysUpTime = '","';"))
