#!/usr/bin/env python
import socket
import threading

import sbs

TCP_IP = '10.0.0.198'
TCP_PORT = 30003
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def listen(arg1, stop_event):
    while (not stop_event.is_set()):
        data = s.recv(BUFFER_SIZE)
        mesg = str(data, encoding='utf-8').split('\r\n')
        for l in mesg:
            if l != '':
                # print("received data:", l)
                cols = l.split(',')

                if cols[0] == 'MSG':

                    pass
    s.close()



station = [60.32509, 5.02074]

dust = {}

if __name__ == "__main__":

    thread_stop = threading.Event()
    t = threading.Thread(target=listen, args=(2, thread_stop))
    t.daemon=True
    t.start()
    try:
        while True:
            # TODO:: Please write your application code
            eval(input())
    except KeyboardInterrupt:
        pass
    finally:
        thread_stop.set()