import os, glob
from fileinfo import Fileinfo
import configparser

def scanpath(PATH, hashes):
    filedict = {}
    for filename in glob.iglob("%s\**" % PATH, recursive=True):
        filename = filename.replace('\\', '/')
        relpath = filename[len(PATH):]
        isdir = not os.path.isfile(filename)

        incld = True
        for ign in ignores:
            incld = incld and not ((relpath[1:] + '/').startswith(ign) if isdir else relpath[1:].startswith(ign))
            if not incld:
                break

        if incld and not isdir:

            fileinfo = Fileinfo(hashes, filename)
            for chunk in open(filename, 'rb'):
                fileinfo.update(chunk)
            filedict[fileinfo.hasobj[hashes[0]].hexdigest()] = fileinfo
    return filedict

# load config
config = configparser.ConfigParser()
config.read('scantree.cfg')
PATH = config.get('Options', 'PATH') if config.has_option('Options', 'PATH') else os.path.dirname(os.path.abspath(__file__))
ignore = config.get('Options', 'ignore') if config.has_option('Options', 'ignore') else ''

PATH = PATH.replace('\\', '/')
ignores = ignore.replace('\\', '/').split(';')

print(' ' * 100, 'Binary', '{:>10}'.format('Size'))
print(119 * '-')

PATH = os.path.dirname(os.path.abspath(__file__)) + '/test'

hashes = ['SHA1']
data = scanpath(PATH, hashes)

import json
# Writing JSON data
with open('dump/filedict.json', 'w') as f:
     json.dump(data, f)

# import html
# hf = open('dump/index.html', 'w')
# print('<html><body><table>', file=hf)
# for key, val in filedick.items():
#     if not val.binary:
#         print('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (os.path.relpath(val.filename, PATH), val.fsize, key), file=hf)
# print('</table></body></html>', file=hf)


# import sys
# import codecs
# import html
# sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')
# hf = open('filsrc.html', 'w+')
# print('<html><body><table>', file=hf)
# for key, val in filedick.items():
#     if not val.binary:
#         print('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (key, val.filename, val.fsize), file=hf)
#         print('<tr><td colspan="3">', file=hf)
#         try:
#             print(html.escape(val.text), file=hf)
#         except:
#             print(key, str(val).rstrip(), 'failed printing text to html')
#         finally:
#             print('</td></tr>', file=hf)
# print('</table></body></html>', file=hf)