#!/usr/bin/env python3
import time
import cv2
import sys

class Camera(threading.thread):
    def __init__(self, _loop = None, _teardown = None):
        threading.Thread.__init__(self)
        self.loop = _loop
        self.teardown  = _teardown
        self.running = True
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        try:
            i = 0
            while cap.isOpened():
                _, frame = cap.read()
                if _loop:
                    _loop(frame, i)
                i += 1
                cv2.waitKey(1)
                if running == False:
                    break
        finally:
            cap.release()
            if _teardown:
                _teardown()
    def stop(self):
        self.running = False
if __name__ == "__main__":
    prevtime = 0
    def callback(image, loopRun):
        global prevtime
        cv2.imshow("Frame", image)
        time.sleep(0.02)
        print((time.time()-prevtime)*1000,"ms")
        prevtime = time.time()
    test_camera = Camera(callback)
    print("Starting live preview...")
    # runs a forever loop on main thread
    # callback will be called in evert loop run
    test_camera.start()
    try:
        while True:
            continue
    except KeyboardInterrupt:
        test_camera.stop()
        test_camera.join()
