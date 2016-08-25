import hashlib # Hash algorithms always present in hashlib: md5(), sha1(), sha224(), sha256(), sha384(), and sha512(). Additional algorithms may be available from OpenSSL library
import binascii
import base64
import traceback
import re

def md5(hash):
    return hashlib.md5(hash).digest()

def md5iter(times, hash):
    for _ in range(times):
        hash = md5(hash)
    return hash

def sha1(hash):
    return hashlib.sha1(hash).digest()

def strtoupper(str):
    return str.upper()

def base64_encode(str):
    return base64.b64encode(str)

def strrev(str):
    return str[::-1]

def decode(line, usr, pwd, salt):
    funk = line.split(',')[0]
    func = funk.replace('- ', '')
    func = func.replace('$pass', "b'" + pwd + "'")
    func = func.replace('$salt', "b'" + salt + "'")
    func = func.replace('.', ' + ')
    func = func.replace('$username', "b'" + usr + "'")

    pattern = r'(.*)([0-9]+)(\sx\s)([A-Z|a-z|0-9]+)([(])(.*)'  # 6 x md5($pass)
    match = re.match(pattern, func)#, re.I | re.U)
    if hasattr(match, 'group'):
        func = match.group(4) + 'iter(' + match.group(2) + ', ' + match.group(6)

    try:
        result = [repr(binascii.hexlify(eval(func))), func, funk]
    except:
        formatted_lines = traceback.format_exc().splitlines()
        result = ["b'" + '0' * 32 + "' ", func, formatted_lines[-1] + ' ' + funk ]
    return result
