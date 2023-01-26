import serial
from .parser import GPGGAParser


def get_coords():
    try:
        s = serial.Serial("/dev/ttyS0")
        s.baudrate = 9600
    except:
        return 0, 0
    while True:
        d = s.readline().decode()
        if d.startswith("$GPGGA"):
            p = GPGGAParser(d)
            return (p.latitude, p.longitude)
