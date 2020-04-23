from picamera import PiCamera
import time

class Camera:
    def __init__(self, name):
        self.camera = PiCamera()
        self.camera.annotate_text = name
        self.camera.rotation = 40
        self.camera.resolution = (1640,922)
        self.camera.framerate = 40
    def takePicture(self, fileName):
        self.camera.capture(fileName)
    def startLiveFeed(self):
        self.camera.start_preview()
    def stopLiveFeed(self):
        self.camera.stop_preview()
if __name__ == "__main__":
    test_camera = Camera("Car Front")
    print("Testing image capture time...")
    start = time.time()
    test_camera.takePicture('/home/pi/Documents/EML_Car/camera_test/testimage.jpg')
    end = time.time()
    print("Taking a picture took: ",end-start)
    print("Starting live preview...")
    test_camera.startLiveFeed()
    try:
        while True:
            continue
    except KeyboardInterrupt:
        test_camera.stopLiveFeed()
        print("live preview stopped")
