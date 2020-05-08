#!/usr/bin/env python3
import serial as ser
import time
import threading

PWM_MASK = 0x7FFF
CH_MASK = 0x8000

# This class uses an Arduino to precisley measure the pulse length of the Receivers PWM pins.
class RCReceiver(threading.Thread):
    def __init__(self, port, baudrate=9600, validRange=range(800,2200),
                 _callback = None):
        threading.Thread.__init__(self)
        self.serial = ser.Serial()
        self.serial.port = port
        self.serial.baudrate = baudrate
        self.serial.timeout = 0
        self.validRange = validRange
        self.channelData = [0.0, 0.0]
        self.running = True
        self.callback = _callback
    def getChannelData(self):
        return self.channelData
    def stop(self):
        self.running = False
    def run(self):
        self.serial.open()
        while self.running:
            if(self.serial.in_waiting >1):
                try:
                    line = int(self.serial.readline().decode("utf-8"))
                    ch = (line & CH_MASK) >> 15
                    pwm = line & PWM_MASK
                    if pwm in self.validRange:
                        self.channelData[ch] = pwm
                        if self.callback:
                            self.callback(ch, pwm)
                except ValueError:
                    continue
        self.serial.close()
if __name__ == '__main__':
    test_receiver = RCReceiver(port="/dev/ttyUSB0", baudrate=115200, validRange=range(800,2200))
    print("opening serial port and starting thread...")
    test_receiver.start()
    try:
        while True:
            channelData = test_receiver.getChannelData()
            print(channelData)
            time.sleep(0.02)
    except KeyboardInterrupt:
        print("stopping thread")
        test_receiver.stop()
        print("waiting for thread to stop")
        test_receiver.join()
