import requests
from FunCom import find_between
from session import login, host, cookies

if login.status_code == requests.codes.ok and cookies['SESSION'] is not '':
    print('=~=~=~=~=~=~=~=~=~=~=~=                               =~=~=~=~=~=~=~=~=~=~=~=')
    f = requests.get('http://%s/pages/maintenance/disagnostic/pingTest.html' % host, cookies=login.cookies)
    form_action = find_between(f.text, '<form  action="', '" method="post">')
    sessionKey = find_between(f.text, '<input type="hidden" name="sessionKey" id="sessionKey" value="', '">')

    print(form_action, sessionKey)
