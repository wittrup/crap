# import pickle
# with open('filsrc.dmp', "wb") as output:
#     pickle.dump(filedick, output)


import cPickle as pickle
from fileinfo import Fileinfo
# to deserialize the object
with open('filsrc.dmp', 'rb') as input:
    filedick = pickle.load(input) # protocol version is auto detected

