answ = '4cbf522049d7cc0e46a337fcc3cad331'
match = ''

import hashlib
import binascii

import hashlib # Hash algorithms always present in hashlib: md5(), sha1(), sha224(), sha256(), sha384(), and sha512(). Additional algorithms may be available from OpenSSL library

hashdict = {'TelenorRemoteAdmin': '4caacf3fd454786eed5e429b7b40ce2d', 'qwer1234': '4cbf522049d7cc0e46a337fcc3cad331', 'dfgt5653': 'c46b1eaa51f853eeb8eae453ba620657'}


def md5(hash):
    return hashlib.md5(hash).digest()

qw = hashlib.md5(b"qwer1234")
qv = hashlib.md5(b"qwer1234")
qm = md5(b"qwer1234")

def md5iter(times, hash):
    for _ in range(times):
        hash = md5(hash)
    return binascii.hexlify(hash)

for i in range(6):
    print(qw.hexdigest(), qv.hexdigest(), binascii.hexlify(qm))

    qw.update(qw.digest())
    qv.update(bytes(qv.hexdigest(), 'ascii'))
    qm = md5(qm)

    if qw.hexdigest == answ:
        match = str(i)
    if qv.hexdigest == answ:
        match = str(i)

print('DONE', match)
print(md5iter(6, b'qwer1234') )

# if __name__ == '__main__':
#     usr = 'admin'
#     pwd = 'qwer1234'
#
#     s1 = '- md5(md5($pass)), Double MD5'
#     s2 = '- md5(md5($pass).$pass)'
#     s3 = '- md5($username.0.$pass)'
#
#     decode(s1, usr, pwd, '')
#     decode(s2, usr, pwd, '')
#     decode(s3, usr, pwd, '')
