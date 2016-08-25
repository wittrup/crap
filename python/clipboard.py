from time import sleep
import sys
import os
sys.path.append(os.path.abspath("SO_site-packages"))

import pyperclip

import re
pattern = r'(\d{2}\/\d{4}) - (\d{2}\/\d{4})\t([\w -ÆØÅæøå]+)\t([\w -ÆØÅæøå]+)\t([\w -ÆØÅæøå]+)'

from keyboard import *

recent_value = ""
selfchange = False
while True:
    clp_value = pyperclip.paste()
    if clp_value != recent_value and not selfchange:
        recent_value = clp_value
        match = re.match(pattern, clp_value, re.I | re.U)
        if hasattr(match, 'group'):
            values = list(match.groups())
            for i in [0, 1]:
                values[i] = '01.' + values[i].replace('/', '.')
            out = list(zip(values, ['\t\t', '\t\t', '\t\t', '\t', '\t']))
            print(out)
            sleep(2)
            for tup in out:
                pyperclip.copy(tup[0])
                PressKey(VK_CONTROL)
                PressKey(key_V)
                ReleaseKey(key_V)
                ReleaseKey(VK_CONTROL)
                sleep(0.05)

                for c in tup[1]:
                    PressKey(ord(c))
                    ReleaseKey(ord(c))
                    sleep(0.05)

    sleep(0.1)