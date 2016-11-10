import sys,requests
"""Small script that takes two arguments <consumptionMeterId> and <consumptionReading> and posts to BKK, a norwegian power company"""

if len(sys.argv) < 3:
    sys.exit('Arguments required <consumptionMeterId> and <consumptionReading>')
if len(sys.argv[1]) != 8:
    sys.exit('<consumptionMeterId> must be 8 digits')
host = r'https://www.bkk.no/api/message'
head = {'content-type': 'application/json'}
data = {"messageType":"consumption-registration","data":{"customerName":"","customerPhone":"","isValid":False,"isDisabled":False,"isSubmitting":False}}
data['data'].update(dict(zip(['consumptionMeterId', 'consumptionReading'], sys.argv[1:])))
r = requests.post(host, headers=head, json=data, timeout=2)
print(r)
print(r.text)