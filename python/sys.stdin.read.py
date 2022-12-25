from os.path import isfile
from startup import NewPut
file = 'sys.stdin'
input = NewPut(file).readline if file is not None and isfile(file) else input


