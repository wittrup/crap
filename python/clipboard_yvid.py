"""
Script for fetching youtube video ID as url appear in clipboard
"""

PATTERN=r'(https:\/\/www\.youtube\.com\/watch\?v=)(\w+)'
FORMAT = '%Y-%m-%d %H:%M:%S'

from time import strftime as now
from time import sleep
import sys
import os
from time import strftime, strptime
sys.path.append(os.path.abspath("SO_site-packages"))
import pyperclip
import re

value_recent = ""
selfchange = False
while True:
    value_clp = pyperclip.paste()
    if value_clp != value_recent and not selfchange:
        value_recent = value_clp
        match = re.match(PATTERN, value_clp, re.I | re.U)
        if hasattr(match, 'group'):
            values = list(match.groups())
            print(now(FORMAT), values[1])

    sleep(0.1)
