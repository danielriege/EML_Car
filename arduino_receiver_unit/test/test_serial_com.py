#!/usr/bin/env python3
import serial
import time

PWM_MASK = 0x7FFF
CH_MASK = 0x8000

ser = serial.Serial('/dev/tty.usbmodem141201', 115200, timeout=0)
try:
    while 1:
        if(ser.in_waiting >1):
            try:
                line = int(ser.readline().decode("utf-8"))
                ch = (line & CH_MASK) >> 15
                pwm = line & PWM_MASK
                if pwm in range(800,2200):
                    print(ch,": ", pwm)
            except ValueError:
                continue

except KeyboardInterrupt:
    ser.close()
