import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
section = config.sections()[0]
host = config.get(section, 'host', fallback='10.0.0.138')
usr = config.get(section, 'user', fallback='admin')
pwd = config.get(section, 'pass', fallback='')
if pwd == '':
    exit('pass must be set in config.ini')

details = {"AuthName": usr, "AuthPassword": pwd}
login = requests.Session()
login = login.post('http://%s/login/login-page.cgi' % host, data=details)

cookies = {}
for item in str(login.headers['Set-Cookie']).split(';'):
    key, val = item.lstrip().split("=", 1)
    cookies[key] = val