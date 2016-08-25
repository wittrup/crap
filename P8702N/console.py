#!/usr/bin/env python
import socket
import threading

import sbs

TCP_IP = '10.0.0.184'
TCP_PORT = 10001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

pipeaway = {'kern.alert': None, 'daemon.warn': None, 'CMS MDM': None}

for key in pipeaway:
    pipeaway[key] = open('pipes' + key, 'w')

def listen(arg1, stop_event):
    mesg = ''
    while (not stop_event.is_set()):
        data = s.recv(BUFFER_SIZE)
        mesg += str(data, encoding='utf-8')
        if '\r\n' in mesg:
            msg = mesg.rstrip()
            mesg = ''
            printto = None
            for key in pipeaway:
                if key in msg:
                    printto = pipeaway[key]
            print(msg, file=printto)
    s.close()



def send(msg):
    s.send(str(msg + '\r\n').encode())

dust = {}

users = ["supervisor", "support", "user", "nobody", "zyuser", "root", "wittrup"]

if __name__ == "__main__":

    thread_stop = threading.Event()
    t = threading.Thread(target=listen, args=(2, thread_stop))
    t.daemon=True
    t.start()
    try:
        while True:
            # TODO:: Please write your application code
            for user in users:
                for i in range(2):
                    send(user)

            eval(input())
    except KeyboardInterrupt:
        pass
    finally:
        thread_stop.set()