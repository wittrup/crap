from os.path import isfile, exists, abspath, dirname
from os import chdir, getcwd
from startup import EnumWindows, EnumWindowsProc, foreach_window, similar, windows
from pywinauto import application
from keyboard import PressKey, ReleaseKey, VK_TAB, VK_SHIFT
from time import time, sleep
import re
import pyotp


ctok = {'c': 67, 'z': 90, 'j': 74, 'x': 88, 'v': 86, 'r': 82, 'p': 80, 'f': 70, 'q': 81, 'y': 89, 'k': 75, 't': 84, 'd': 68, 'h': 72, 'l': 76, 'i': 73, 'm': 77, 'a': 65, 's': 83, 'u': 85, 'g': 71, 'e': 69, 'w': 87, 'n': 78, 'b': 66, 'o': 79}
timeout = 5
chdir(dirname(abspath(__file__))) # Change the scripts working directory to the script's own directory
file = 'ignore/Cisco AnyConnect.txt'
print('looking for', file, 'in', getcwd())
if exists(file):
    password, secret = [l.strip() for l in open(file).readlines()]
    otp = pyotp.TOTP(secret)
    del secret
else:
    input('settings file (%s) not found' % file) # wait for user input before exit
	exit()
path = "%PROGRAMFILES(x86)%\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe"
path = r'C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe'
app = application.Application()
sleep(1)
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
        sleep(0.05)
    PressKey(0x0D)
    ReleaseKey(0x0D)

start = time()
while not re.match(pattern, l[0][1]):
    sleep(0.1)
    if time() > start + timeout:
        input('Waiting too long for %s prompt' % cac)
		exit() # wait for user input before exit
    EnumWindows(EnumWindowsProc(foreach_window), 0)
    l = sorted([similar(title, cac) for title in windows], reverse=True)[:2]

print(otp.now())
for c in password + '\t' + otp.now() + '\t\r':
    if c.isupper():
        PressKey(VK_SHIFT)
    if c in ctok:
        PressKey(ctok[c])
        ReleaseKey(ctok[c])
    else:
        PressKey(ord(c))
        ReleaseKey(ord(c))
    if c.isupper():
        ReleaseKey(VK_SHIFT)
    sleep(0.05)
