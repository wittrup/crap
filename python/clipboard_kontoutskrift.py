from time import sleep
import sys
import os
from time import strftime, strptime
sys.path.append(os.path.abspath("SO_site-packages"))

import pyperclip

import re
PATTERN = r'\t(\d{2}\.\d{2}\.\d{4})\t(KONTOUTSKRIFT)'

from keyboard import *

value_recent = ""
selfchange = False
while True:
    value_clp = pyperclip.paste()
    if value_clp != value_recent and not selfchange:
        value_recent = value_clp
        match = re.match(PATTERN, value_clp, re.I | re.U)
        if hasattr(match, 'group'):
            values = list(match.groups())
            value_new = strftime('%Y-%m-%d', strptime(values[0], '%d.%m.%Y')) + ' ' + values[1]
            print('CHANGE', value_clp, '= TO =', value_new)
            pyperclip.copy(value_new)

    sleep(0.1)
