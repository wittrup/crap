from time import strftime as now
import threading
import serial


FORMAT = '%Y-%m-%d %H:%M:%S'
ser = serial.Serial('COM4', baudrate=57600)

def log(data, file='sim800.log'):
    with open(file, 'a+') as f:
        f.write(now(FORMAT) + ' ' + str(data) + '\n')
        f.close()

def read_from_port(ser):
    while True:
        data = ser.readline().rstrip()
        print(data)
        log(b'<< ' + data)


thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

def send(command):
    data = bytes(command + "\r", encoding='ascii')
    ser.write(data)
    log(b'>> ' + data)

while True:
    try:
        query = input()
        if query.upper().startswith("AT"):
            send(query)
        elif query.upper() == "SEND TIME":
            z = float(now("%z")[:3] + '.' + now("%z")[3:]) * 4
            time = now("%y/%m/%d,%H:%M:%S") +  "{:+03.0f}".format(z)
            print("sending time %s" % time)
            send('AT+CCLK="%s"' % time)
        elif query.upper() == "TIME":
            send("AT+CCLK?")
        elif query.upper() == "ACTIVATE":
            send('AT+CFUN=1')
            send('AT+SAPBR=3,1,"CONTYPE","GPRS"')
            send('AT+SAPBR=3,1,"APN","telenor"')
            send('AT+SAPBR=1,1')
            send('AT+SAPBR=2,1')
    except (KeyboardInterrupt, SystemExit, EOFError):
        break