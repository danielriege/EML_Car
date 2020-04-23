import serial as ser
import time

PWM_MASK = 0x7FFF
CH_MASK = 0x8000

# This class uses an Arduino to precisley measure the pulse length of the Receivers PWM pins.
class RCReceiver:
    def __init__(self, port, baudrate=9600, validRange=range(1000,2000)):
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
        print(self.serial.readline().decode("utf-8"))
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
        
if __name__ == '__main__':
    test_receiver = RCReceiver(port="/dev/ttyUSB0", baudrate=115200, validRange=range(0,20000))
    print("opening serial port...")
    if test_receiver.startListening():
        print("serial port is open and listening started")
    else:
        print("serial port opening failed")
        exit()
    try:
        while True:
            data = test_receiver.read()
            print(data)
    except KeyboardInterrupt:
        if test_receiver.stopListening():
            print("serial port closed sucessfully.")
        else:
            print("serial port closing failed!")
