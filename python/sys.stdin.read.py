from os.path import isfile
from startup import newput
file = 'sys.stdin'
input = newput(file).readline if file is not None and isfile(file) else input


