from os.path import isfile, exists
from startup import EnumWindows, EnumWindowsProc, foreach_window, similar, windows
from pywinauto import application
from keyboard import PressKey, ReleaseKey, VK_TAB
from time import time, sleep
import re
import pyotp


timeout = 5
file = 'ignore/Cisco AnyConnect.txt'
if exists(file):
    password, secret = [l.strip() for l in open(file).readlines()]
    otp = pyotp.TOTP(secret)
    del secret
else:
    exit('settings file (%s) not found' % file)
path = "%PROGRAMFILES(x86)%\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe"
path = r'C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe'
app = application.Application()
app.start(path)
cac = r'Cisco AnyConnect'
smc = r'Cisco AnyConnect Secure Mobility Client'
pattern = r'Cisco AnyConnect (\|) ([\w ]+)'
EnumWindows(EnumWindowsProc(foreach_window), 0)
l = sorted([similar(title, cac) for title in windows], reverse=True)[:2]

if l[0][1] == smc:
    print('Found:', smc)
    for _ in range(3):
        PressKey(VK_TAB)
        ReleaseKey(VK_TAB)
    PressKey(0x0D)
    ReleaseKey(0x0D)

start = time()
while not re.match(pattern, l[0][1]):
    sleep(0.1)
    if time() > start + timeout:
        exit('Waiting too long for %s prompt' % cac)
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    l = sorted([similar(title, cac) for title in windows], reverse=True)[:2]

print(otp.now())
for c in password + '\t' + otp.now() + '\t\r':
    PressKey(ord(c))
    ReleaseKey(ord(c))
    sleep(0.1)
