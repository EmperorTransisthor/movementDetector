import os, sys
from pickle import TRUE
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX127x
import wiringpi
import time

ssPin = 6
dio0 = 7
RST = 0
CHANNEL = 0
freq = 868100000
message = [None]*256

def SetupLoRa():
    wiringpi.digitalWrite(RST, 1)
    time.sleep(0.1)
    wiringpi.digitalWrite(RST, 0)
    time.sleep(0.1)
    
    wiringpi.digitalWrite(RST, 0)
    time.sleep(0.1)
    wiringpi.digitalWrite(RST, 1)

    time.sleep(0.1)

    #sx1276
    print("SX1276 detected, starting.\n")
    opmode(0x00)
    #set frequency
    frf = 31

    writeReg(0x06,(frf>>16))
    writeReg(0x07,(frf>>8))
    writeReg(0x08,(frf>>0))
    writeReg(0x39, 0x34) #LoRaWAN public sync word
    writeReg(0x1F,0x08)
    writeReg(0x23,0x80)
    writeReg(0x22,0x40)
    writeReg(0x24,0xFF)
    writeReg(0x0D, int.from_bytes(readReg(0x0F),"big"))
    writeReg(0x0C, 0x23)

def readReg(addr):
    spibuf = [None] * 2
    selectreceiver()
    spibuf[0] = addr & 0x7F
    spibuf[1] = 0x00
    recvData = wiringpi.wiringPiSPIDataRW(CHANNEL,bytes(spibuf))
    unselectreceiver()
    return recvData[1]

def selectreceiver():
    wiringpi.digitalWrite(ssPin, 0)

def unselectreceiver():
    wiringpi.digitalWrite(ssPin, 1)

def opmode (mode):
    reg = readReg(0x01)
    mode = mode.to_bytes(2, 'big')
    eight = 8
    eight = eight.to_bytes(2, 'big')
    and_op = bitwise_and_bytes(reg, eight)
    eq = bitwise_or_bytes(and_op, mode)
    eq = int.from_bytes(eq, "big")
    writeReg(0x01, eq)

def writeReg(addr,value):
    spibuf = [None] * 2
    spibuf[0] = addr | 0x80
    spibuf[1] = value
    selectreceiver()
    print(spibuf)
    wiringpi.wiringPiSPIDataRW(CHANNEL, bytes(spibuf))
    unselectreceiver()

def opmodeLora():
    u = 0x80
    u |= 0x8;   #TBD: sx1276 high freq
    writeReg(0x01, u)

def receive(payload):

    writeReg(0x12, 0x40)
    irqflags = int.from_bytes(readReg(0x12), "big")

    if((irqflags & 0x20) == 0x20):
        print("CRC error\n")
        writeReg(0x12, 0x20)
        return False
    else:
        currentAddr = readReg(0x10)
        currentAddr = int.from_bytes(currentAddr, "little")
        receivedCount = readReg(0x13)
        global receivedbytes
        receivedbytes = receivedCount
        receivedbytes = int.from_bytes(receivedbytes, "little")
        writeReg(0x0D, currentAddr)
        for i in range (0, receivedbytes):
            payload[i] = readReg(0x00)
    return True

def receivepacket():
    SNR = 0
    rssicorr = 0
    if(wiringpi.digitalRead(dio0) == 0):
        if(receive(message)):
            value = readReg(0x19)
            bit = 0x80
            if(bitwise_and_bytes(value, bit.to_bytes(2, "big") ) ): #The SNR sign bit is 1
                #Invert and divide by 4
                value = ( ( ~value + 1 ) & 0xFF ) >> 2
                SNR = -value
            else:
                #Divide by 4
                SNR = ( value & 0xFF ) >> 2
            
            rssicorr = 157
            
            print(f"Packet RSSI: {readReg(0x1A)-rssicorr} ")
            print(f"RSSI: {readReg(0x1B)-rssicorr}")
            print(f"SNR: {SNR}")
            print(f"Length: {int(receivedbytes)}")
            print("\n")
            print(f"Payload: {message}\n")

def bitwise_and_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") & int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

def bitwise_or_bytes(a, b):
    result_int = int.from_bytes(a, byteorder="big") | int.from_bytes(b, byteorder="big")
    return result_int.to_bytes(max(len(a), len(b)), byteorder="big")

wiringpi.wiringPiSetup()
wiringpi.pinMode(ssPin, 1)
wiringpi.pinMode(dio0, 0)
wiringpi.pinMode(RST, 0)

wiringpi.wiringPiSPISetup(CHANNEL, 500000)
SetupLoRa()
opmodeLora()
opmode(0x01)
opmode(0x05)
print(f"Listening at SF{7} on {freq/1000000} Mhz.\n")
print("------------------\n")
while(1):
    receivepacket()
    time.sleep(0.01)
    

