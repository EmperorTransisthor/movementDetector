import serial
from time import sleep
from .parser import GPGGAParser

s = serial.Serial("/dev/ttyS0")
s.baudrate = 9600


def get_coords():
    while True:
        d = s.readline().decode()
        if d.startswith("$GPGGA"):
            p = GPGGAParser(d)
            return (p.latitude, p.longitude)
