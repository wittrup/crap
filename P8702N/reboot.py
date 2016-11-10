import argparse
import requests


parser = argparse.ArgumentParser()
parser.add_argument('password')
parser.add_argument('--user', help="username here if other than 'admin'", default='admin')
parser.add_argument('--host', help="hostname here if other than '10.0.0.138'", default='10.0.0.138')
args = parser.parse_args()

request = requests.Session()
request.post('http://%s/login/login-page.cgi' % args.host, data={"AuthName": args.user, "AuthPassword": args.password})

if request.cookies:
    request.get('http://%s/pages/tabFW/reboot-rebootpost.cgi' % args.host)
else:
    exit('login not successful')
