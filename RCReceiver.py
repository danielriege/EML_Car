import serial as ser
import time

PWM_MASK = 0x7FFF
CH_MASK = 0x8000

# This class uses an Arduino to precisley measure the pulse length of the Receivers PWM pins.
class RCReceiver:
    def __init__(self, port, baudrate=115200, validRange=range(1000,2000)):
        self.serial = ser.Serial()
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.serial.timeout = 0.021
        self.validRange = validRange
    def startListening(self):
        self.serial.open()
        return self.serial.is_open
    def stopListening(self):
        self.serial.close()
        return not self.serial.is_open
    def read(self):
        result = [0, 0]
        for i in range(2):
            try:
                serLine = int(self.serial.readline().decode("utf-8"))
                ch = (serLine & CH_MASK) >> 15
                pwm = serLine & PWM_MASK
                if pwm in self.validRange:
                    result[ch] = pwm
            except ValueError:
                continue
        return result
