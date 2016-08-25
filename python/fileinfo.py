import binascii
import hashlib
import os

textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
binchars = bytearray({0x7f} | set(range(0x00, 0x20)) - {7,8,9,10,12,13,27})

class Fileinfo():
    def __init__(self, hashes=None, filename=None):
        self.filename = filename if type(filename) == str else ''
        self.hasobj = {}
        if hashes is not None:
            for hash in hashes:
                self.hasobj[hash] = hashlib.new(hash)
        self.crc32 = binascii.crc32(b'')
        self.fsize = 0
        self.binary = True
        self.text = ''

    def update(self, chunk):
        self.fsize += len(chunk)
        for item in self.hasobj:
            self.hasobj[item].update(chunk)
        self.crc32 = binascii.crc32(chunk, self.crc32) & 0xffffffff
        self.binary = self.binary and bool(chunk.translate(None, textchars))
        if not self.binary:
            self.text += chunk.translate(None, binchars).decode('ISO-8859-1')

    def __repr__(self):
        # {'shares': 100, 'price': 542.23, 'name': 'ACME'}
        s = "{"
        s += '"crc32": 0x{:x}, '.format(self.crc32)
        s += '"path": \'{:}\', '.format(self.filename)
        s += '"puretext": {:}'.format('%r' % self.binary)
        s += '}'
        # s = '\t{:8x}'.
        # s += '\t{:50}'.format()
        # s += '\t{:5}'.format('%r' % self.binary)
        # s += '\t{:10}'.format(self.fsize)
        # s += '\n'
        return dict(s)
