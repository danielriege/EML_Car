#!/usr/bin/env python3
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2

class Camera():
    def __init__(self, name):
        self.resolution = (640, 480)
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        #self.camera.framerate = 30
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)
        # camera warm up
        time.sleep(0.1)
        # User calling Camera.start() will start the stream
    def start(self, _loop = None, _teardown = None):
        loopRun = 0
        for frame in self.camera.capture_continuous(self.rawCapture,
                                                    format="bgr",
                                                   use_video_port=True):
            if _loop:
                _loop(frame.array, loopRun)
            key = cv2.waitKey(1) & 0xFF 
            # clear the stream
            self.rawCapture.truncate(0)
            loopRun += 1
            if key == ord('q'):
                if _teardown:
                    _teardown()
                break
if __name__ == "__main__":
    prevtime = 0
    def callback(image, loopRun):
        global prevtime
        cv2.imshow("Frame", image)
        time.sleep(0.02)
        print((time.time()-prevtime)*1000,"ms")
        prevtime = time.time()
    test_camera = Camera("Car Front")
    print("Starting live preview...")
    # runs a forever loop on main thread
    # callback will be called in evert loop run
    test_camera.start(callback)
