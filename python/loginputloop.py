import os
from time import strftime as now


FORMAT = '%Y-%m-%d %H:%M:%S'

if __name__ == '__main__':
    print(now(FORMAT), os.path.dirname(__file__))
    s = input()
    while s:
        with open('log.txt', 'a+') as f:
            f.write(now(FORMAT) + ' ' + s + '\n')
            f.close()
        s = input()