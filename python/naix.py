import encoding
import os, glob
import binascii
import hashlib
"""naix stands for never ascii iso extended
module for determing probablity of text or something like that...
"""
textchars = {7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f}
text = list(textchars)
print(text)

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='',
                        help='source directory (default: current folder)')
    parser.add_argument('-d', '--dest', type=str, default='naix',
                        help='destination directory (default: naix)')

    args = parser.parse_args()
    targpath = os.path.join(os.getcwd(), args.source)

    for filename in glob.iglob("%s\**" % targpath, recursive=True):

        relpath = filename[len(targpath):]

        fsize = os.path.getsize(filename)
        if os.path.isfile(filename):
            crc32 = binascii.crc32(b'')
            hashes = ['MD5', 'SHA1', 'SHA256', 'SHA512', 'SHA384']
            hasobj = {}
            for hash in hashes:
                hasobj[hash] = hashlib.new(hash)

            f = open(filename, 'rb')

            s = ''
            # peakwidth = 1
            # rising_edge = False
            # startpos = 0
            # i = 0
            for chunk in f:
                for c in chunk:
                    if c in text:
                        s += chr(c)
                    # if c in text: # char is text
                    #     rising_edge = True
                    #     startpos = i
                    # else:
                    #     if rising_edge: # this is falling edge
                    #         rising_edge = False
                    #         if startpos < i - peakwidth: # signal is wider than peak limit
                    #             out += [startpos, i - peakwidth] # append to list
                # if rising_edge and startpos <= i -peakwidth:
                #     out += [startpos, i]
                # i += 1

                for item in hasobj:
                    hasobj[item].update(chunk)
                crc32 = binascii.crc32(chunk, crc32) & 0xffffffff

            print('{:<32}'.format(relpath), '{:<16}'.format(fsize), '{:>8x}'.format(crc32), hasobj['MD5'].hexdigest(), hasobj['SHA1'].hexdigest())
            # print('{:<32}'.format(relpath), '{:<16}'.format(fsize))
            # out=None
            # print(s, file=out)


if __name__ == '__main__':
    main()