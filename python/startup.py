"""should be added to Environmental Variable PYTHONSTARTUP so it runs at beginning of every python console"""
import os, socket, struct, json, sys
import threading
from time import sleep
from difflib import SequenceMatcher

UDP = 0
TCP = 1
MCAST = 2

def similar(a, b):
    subst = a.lower() in b.lower() or b.lower() in a.lower() # One string in the other weighs more than stringmatching
    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio * (subst + 0.5), a, b

class newput():
    def __init__(self, file):
        self.file = open(file)
    def readline(self):
        return self.file.readline().rstrip()

def listinput(file=None,l=[]):
    """Generate list from every line of input until KeyboardInterrupt, SystemExit, EOFError"""
    _input = newput(file).readline if file is not None and os.path.isfile(file) else input
    last = ''
    while True:
        try:
            data = _input()
            if data == '' and last == '':
                break
            elif data != '':
                l.append(data)
            last = data
        except (KeyboardInterrupt, SystemExit, EOFError):
            break
    return l

class Wipe(object):
    """This class is intended to be used as a console command to clear screen"""
    def __repr__(self):
        os.system('cls' if os.name=='nt' else 'clear')
        return ""

class listenthread(threading.Thread):
    def __init__(self, IP, PORT, SOCK_TYPE, PROTO):
        self.sock = socket.socket(socket.AF_INET, SOCK_TYPE, PROTO)# Internet
        self.address = (IP, PORT)
        self.dase = b''
        if PROTO == socket.IPPROTO_UDP: # if multicast
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if IP:
                self.mreq = struct.pack("4sl", socket.inet_aton(IP), socket.INADDR_ANY)
                self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
            self.sock.bind(('', PORT))
        else: # UDP and TCP
            self.sock.bind((IP, PORT))
        self.sock_type = SOCK_TYPE
        if SOCK_TYPE == socket.SOCK_STREAM:
            self.sock.listen(1)
        super(listenthread, self).__init__()
        self._stop = threading.Event()

    def close(self):
        self.sock.close()

    def run(self):
        while not self._stop.isSet():
            try:
                if self.sock_type == socket.SOCK_STREAM:
                    conn, addr = self.sock.accept()
                    print('Connection address:', addr)
                    recv_data = conn.recv(1024)
                else:
                    recv_data, addr = self.sock.recvfrom(1024)
                if recv_data and recv_data != self.dase:
                    print(recv_data, 'from', addr)
            except:
                self._stop.set()

    def send(self, text):
        self.dase = bytes(text, 'ascii')
        if self.sock_type == socket.SOCK_STREAM: # TCP
            self.sock.send(self.dase)
        else:
            self.sock.sendto(self.dase, self.address)

def _listen(IP, PORT, SOCK_TYPE=socket.SOCK_DGRAM, PROTO=0):
    server_thread = listenthread(IP, PORT, SOCK_TYPE, PROTO)
    server_thread.daemon = True
    server_thread.start()
    try:
        while True:
            query = input()
            if query.upper() == 'CLEAR':
                repr(Wipe())
            else:
                server_thread.send(query)
    except (KeyboardInterrupt, SystemExit):
        print('Closing socket...')
        server_thread.close()
    print('Closed...')

def listen(TYPE, IP, PORT):
    if TYPE == TCP:
        _listen(IP, PORT, socket.SOCK_STREAM)
    elif TYPE == MCAST:
        _listen(IP, PORT, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    else:
        _listen(IP, PORT)

clear = Wipe()

if os.name=='nt':
    import ctypes
    FindWindow = ctypes.windll.user32.FindWindowW
    ShowWindow = ctypes.windll.user32.ShowWindow

    window_ignore = ['', 'Default IME', 'MSCTFIME UI', 'GDI+ Window', 'CWNPTransportImpl', 'DDE Server Window',
                     'Task Host Window', 'Windows Push Notifications Platform', 'Windows Shell Experience Host',
                     'Battery Meter', 'BluetoothNotificationAreaIconWindowClass']
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    def foreach_window(hwnd, lParam):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        title = buff.value
        if title not in window_ignore:
            windows[title] = bool(IsWindowVisible(hwnd))
        return True
    windows = {}


    def hide(s):
        """       Hide a window
        :param s: Target window title
        :return:  None
        :OS:      WINDOWS"""
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        s = max(similar(title, s) for title in windows)[1]
        ShowWindow(FindWindow(None, s), 0)
    def show(s):
        """       Show a window
        :param s: Target window title
        :return:  None
        :OS:      WINDOWS"""
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        s = max(similar(title, s) for title in windows)[1]
        ShowWindow(FindWindow(None, s), 5)