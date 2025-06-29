"""
Add to Environmental Variable PYTHONSTARTUP to run at beginning of every python console
Requirements: pip install pyotp
"""
from __future__ import print_function
from time import sleep
import os
import socket
import struct
import sys
import threading
from difflib import SequenceMatcher
import hashlib
import pyotp


UDP = 0
TCP = 1
MCAST = 2

BOTTOM = 1      # Places window at bottom of Z order. If the hWnd parameter identifies a topmost window,
                # window loses its topmost status and is placed at the bottom of all other windows.
NOTOPMOST = -2  # Places the window above all non-topmost windows (that is, behind all topmost windows).
                # This flag has no effect if the window is already a non-topmost window.
TOP=0           # Places the window at the top of the Z order.
TOPMOST = -1    # Places the window above all non-topmost windows.
                # The window maintains its topmost position even when it is deactivated.



def conv(value, fromLow=0, fromHigh=0, toLow=0, toHigh=0, func=None):
    result = (value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow
    if func is None:
        return result
    else:
        return func(result)


def similar(a, b):
    subst = a.lower() in b.lower() or b.lower() in a.lower() # One string in the other weighs more than stringmatching
    ratio = SequenceMatcher(None, a, b).ratio()
    return ratio * (subst + 0.5), a, b


class NewPut:
    def __init__(self, file):
        self.file = open(file)

    def readline(self):
        return self.file.readline().rstrip()


def listinput(file=None, ls=None):
    """Generate list from every line of input until KeyboardInterrupt, SystemExit, EOFError"""
    _input = NewPut(file).readline if file is not None and os.path.isfile(file) else input
    last = ''
    if ls is None:
        ls = []
    while True:
        try:
            data = _input()
            if data == '' and last == '':
                break
            elif data != '':
                ls.append(data)
            last = data
        except (KeyboardInterrupt, SystemExit, EOFError):
            break
    return ls


class ListenThread(threading.Thread):
    def __init__(self, IP, PORT, SOCK_TYPE, PROTO):
        self.sock = socket.socket(socket.AF_INET, SOCK_TYPE, PROTO)  # Internet
        self.sock_udp = None
        self.address = (IP, PORT)
        self.dase = b''
        if PROTO == socket.IPPROTO_UDP:  # if multicast
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if IP:
                self.mreq = struct.pack("4sl", socket.inet_aton(IP), socket.INADDR_ANY)
                self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
            self.sock.bind(('', PORT))
        else:  # UDP and TCP
            self.sock.bind((IP, PORT))
        self.sock_type = SOCK_TYPE
        if SOCK_TYPE == socket.SOCK_STREAM:  # TCP
            self.sock.listen()
            self.clients = []
        super(ListenThread, self).__init__()
        self.alive = threading.Event()
        self.alive.set()
        self._UDP_endpoints = []
        self.lock = threading.Lock()

    def join(self, timeout=None):
        self.sock.close()
        self.alive.clear()
        threading.Thread.join(self, timeout)

    def run(self):
        while self.alive.is_set():
            try:
                if self.sock_type == socket.SOCK_STREAM:  # TCP
                    print('Waiting for connections...')
                    conn, addr = self.sock.accept()
                    with self.lock:
                        self.clients.append(conn)
                    threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
                else:
                    recv_data, addr = self.sock.recvfrom(1024)
                    if recv_data and recv_data != self.dase:
                        if addr not in self._UDP_endpoints:
                            print(addr, type(addr))
                            self._UDP_endpoints.append(addr)
                        print(recv_data, 'from', addr)
            except:  # PEP 8: E722 do not use bare 'except' Too broad exception clause
                self.alive.clear()
        print('SERVER: Thread stopped')

    def handle_client(self, conn, addr):
        try:
            while self.alive.is_set():
                data = conn.recv(1024)
                if not data:
                    break
                print(f"[CLIENT {addr}] {data.decode()}")
        except Exception as e:
            print(f"[CLIENT ERROR] {addr}: {e}")
        finally:
            with self.lock:
                self.clients.remove(conn)
            conn.close()
            print(f"[CLIENT] {addr} disconnected")

    def send(self, text):
        if sys.version_info < (3, 0):
            self.dase = bytes(text)
        else:
            self.dase = bytes(text, 'ascii')
        if self.sock_type == socket.SOCK_STREAM:  # TCP
            for i, client in reversed(list(enumerate(self.clients))):
                try:
                    conn, addr = client
                    conn.sendall(self.dase)
                except:
                    print('SERVER:', addr, 'lost.')
                    self.clients.pop(i)
            for addr in self._UDP_endpoints:
                try:
                    self.sock_udp.sendto(self.dase, addr)
                    print('UDP send from TCP', addr, self.dase)
                except Exception as e:
                    print(addr, e)
        elif self.sock_type == socket.SOCK_DGRAM:
            for addr in self._UDP_endpoints:
                self.sock.sendto(self.dase, addr)
                print('UDP send from UDP', addr, self.dase)
        else:
            self.sock.sendto(self.dase, self.address)

    def add_udp(self, addr):
        if self.sock_udp is None:
            self.sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            self.sock_udp.bind(('0.0.0.0', 0))
        if addr not in self._UDP_endpoints:
            self._UDP_endpoints.append(addr)


def _listen(IP, PORT, SOCK_TYPE=socket.SOCK_DGRAM, PROTO=0):
    server_thread = ListenThread(IP, PORT, SOCK_TYPE, PROTO)
    server_thread.daemon = True
    server_thread.start()
    try:
        while True:
            query = raw_input() if sys.version_info < (3, 0) else input()
            splits = list(map(str.upper, query.split()))
            if query.upper() == 'CLEAR':
                repr(Wipe())
            elif query and splits[0] == 'UDP':
                server_thread.add_udp((splits[1], int(splits[2])))
            else:
                server_thread.send(query)
    except (KeyboardInterrupt, SystemExit):
        print('Closing socket...')
        server_thread.join()
    print('Closed...')


def listen(*kwargs):
    if 3 == len(kwargs):
        TYPE, IP, PORT = kwargs
        if TYPE == TCP:
            _listen(IP, PORT, socket.SOCK_STREAM)
        elif TYPE == MCAST:
            _listen(IP, PORT, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        else:
            _listen(IP, PORT)
    elif 2 == len(kwargs):
        IP, PORT = kwargs
        _listen(IP, PORT)


class Totp(pyotp.TOTP):
    def __init__(self, s, digits=6, digest=hashlib.sha1):
        if type(s) == str:  # Avoids ERROR: test_match_rfc AttributeError: 'int' object has no attribute 'upper'
            s = ''.join(c for c in s if c.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=")
        pyotp.TOTP.__init__(self, s, digits, digest)


class Wipe(object):
    """This class is intended to be used as a console command to clear screen"""
    def __repr__(self):
        os.system('cls' if os.name=='nt' else 'clear')
        return ""


clear = Wipe()

if os.name == 'nt':
    import ctypes
    from ctypes import wintypes
    FindWindow = ctypes.windll.user32.FindWindowW
    ShowWindow = ctypes.windll.user32.ShowWindow
    GetWindowRect = ctypes.windll.user32.GetWindowRect

    window_ignore = ['', 'Default IME', 'MSCTFIME UI', 'GDI+ Window', 'CWNPTransportImpl', 'DDE Server Window',
                     'Task Host Window', 'Windows Push Notifications Platform', 'Windows Shell Experience Host',
                     'Battery Meter', 'BluetoothNotificationAreaIconWindowClass']
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    SetWindowPos = ctypes.windll.user32.SetWindowPos
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

    def find_window_hwnd(title):
        if type(title) != str:
            return title
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        title = max(similar(window_title, title) for window_title in windows)[1]
        hwnd = FindWindow(None, title)
        print(f"Found '{title}'@{hwnd}")
        return hwnd

    def hide(s):
        """       Hide a window
        :param s: Target window title
        :return:  None
        :OS:      WINDOWS"""
        ShowWindow(find_window_hwnd(s), 0)

    def show(s):
        """       Show a window
        :param s: Target window title
        :return:  None
        :OS:      WINDOWS"""
        ShowWindow(find_window_hwnd(s), 5)

    def place(hwnd, x=0, y=0, cx=0, cy=0, HIA=TOP):
        """
        :param s:   Target window title
        :param x:   The new position of the left side of the window, in client coordinates.
        :param y:   The new position of the top of the window, in client coordinates.
        :param cx:  The new width of the window, in pixels.
        :param cy:  The new height of the window, in pixels.
        :param HIA: hWndInsertAfter
        :return: None   """

        hwnd = find_window_hwnd(hwnd)
        if any([0 == n for n in (x, y, cx, cy)]):
            x, y, cx, cy = winpos(hwnd)
            cx = abs(cx - x)
            cy = abs(cy - y)
        print(x, y, cx, cy)
        # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-setwindowpos
        SetWindowPos(hwnd, HIA, x, y, cx, cy, 4)

    def winpos(hwnd):
        hwnd = find_window_hwnd(hwnd)
        rect = wintypes.RECT()
        GetWindowRect(hwnd, ctypes.pointer(rect))
        return (rect.left, rect.top, rect.right, rect.bottom)
