import requests
import configparser

config = configparser.ConfigParser()
config.read('../ignore/P8702N_config.ini')
section = config.sections()[0]
host = config.get(section, 'host', fallback='10.0.0.138')
usr = config.get(section, 'user', fallback='admin')
pwd = config.get(section, 'pass', fallback='')
if pwd == '':
    exit('pass must be set in P8702N_config.ini')

details = {"AuthName": usr, "AuthPassword": pwd}
login = requests.Session()
login = login.post('http://%s/login/login-page.cgi' % host, data=details)
cookies = login.cookies

if __name__ == '__main__':
    print(cookies)
