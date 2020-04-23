from RCReceiver import RCReceiver
from CarControl import CarControl
import time
from Camera import Camera

CHANNEL_1 = 0
CHANNEL_2 = 1

# SETUP
rec = RCReceiver(port="/dev/ttyUSB0", baudrate=115200)
ctl = CarControl(steering_zero = 1500,
steering_trim = -1.85,
throttle_zero = 1250,
steering_pin = 18,
throttle_pin = 12)
camera = Camera("Car front")

if not rec.startListening():
    print('Error opening Port')
ctl.start()
camera.startLiveFeed()
# LOOP
try:
    while True:
        data = rec.read()
        print(data)
        ctl.steer(data[CHANNEL_1])
        ctl.accelerate(data[CHANNEL_2])
# TERMINATE
except KeyboardInterrupt:
    camera.stopLiveFeed()
    ctl.stop()
    if not rec.stopListening():
        print('Error closing Port')
