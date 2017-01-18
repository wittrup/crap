cmd = r"C:\Users\wittr\sdr\kalibrate-win-release\kal.exe"


import os, re
from subprocess import Popen, PIPE


pattern_band = r'\s*band to scan\s*\((.+)\)'
pattern_chan = r'(chan).+?(\d+).+?([\d.]+)(\w+).+?([\d.]+)(\w+).+?(\w+).+?([\d.]+)'

process = Popen(cmd + ' -h', shell=True, stdout=PIPE)  # To use a pipe with the subprocess module, you have to pass shell=True
(result, err) = process.communicate()
process.wait()  # Wait for process to finish

result = str(result, encoding='ascii')
matches = re.findall(pattern_band, result)

results = {}
for match in matches:
    bands = match.split(', ')
    for band in bands:
        process = Popen(cmd + ' -s ' + band, shell=True, stdout=PIPE, stderr=PIPE)  # To use a pipe with the subprocess module, you have to pass shell=True
        (result, err) = process.communicate()
        process.wait()  # Wait for process to finish
        result = str(result, encoding='ascii')
        channels = re.findall(pattern_band, result)
        for channel in channels:
            channel = list(channel)
            with channel as c:
                c.insert(2, 'freq')
                c.insert(4, 'freqdesignation')
                c.insert(6, 'bandwidth')
                c.insert(8, 'banddesignation')
                channel = dict(zip(c[0::2], c[1::2]))
