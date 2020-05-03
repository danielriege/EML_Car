#!/usr/bin/env python3
import serial as ser
import time

PWM_MASK = 0x7FFF
CH_MASK = 0x8000

# This class uses an Arduino to precisley measure the pulse length of the Receivers PWM pins.
class RCReceiver:
    def __init__(self, port, baudrate=9600, validRange=range(800,2200)):
        self.serial = ser.Serial()
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.serial.timeout = 0
        self.validRange = validRange
    def startListening(self):
        self.serial.open()
        return self.serial.is_open
    def stopListening(self):
        self.serial.close()
        return not self.serial.is_open
    def read(self, channelData):
        if(ser.in_waiting >1):
            try:
                line = int(ser.readline().decode("utf-8"))
                ch = (line & CH_MASK) >> 15
                pwm = line & PWM_MASK
                if pwm in self.validRange:
                    channelData[ch] = pwm
            except ValueError:
                continue

if __name__ == '__main__':
    test_receiver = RCReceiver(port="/dev/ttyUSB0", baudrate=115200, validRange=range(800,2200))
    print("opening serial port...")
    if test_receiver.startListening():
        print("serial port is open and listening started")
    else:
        print("serial port opening failed")
        exit()
    try:
        channelData = [0.0, 0.0]
        while True:
            test_receiver.read(channelData)
            print(channelData)
    except KeyboardInterrupt:
        if test_receiver.stopListening():
            print("serial port closed sucessfully.")
        else:
            print("serial port closing failed!")
