from picamera import PiCamera
import time
class Camera:
    def __init__(self):
        camera = PiCamera()
    def takePicture(self, fileName):
        camera.capture(fileName)
    def startLiveFeed(self):
        camera.start_preview()
    def stopLiveFeed(self):
        camera.stop_preview()
if __name__ == "__main__":
    test_camera = Camera()
    print("Testing image capture time...")
    start = time.time()
    test_camera.takePicture('/camera_test/testimage.jpg')
    end = time.time()
    print("Taking a picture took: ",end-start)
    print("Starting live preview...")
    try:
        while True:
            test_camera.startLiveFeed()
    except KeyboardInterrupt:
        test_camera.stopLiveFeed()
        print("live preview stopped")
