#!/usr/bin/env python3
from tensorflow.keras.models import load_model
#import matplotlib.image as mpimg
import cv2
import numpy as np

class LaneNavigator:
        def __init__(self, model_path):
            self.model = load_model(model_path)
        def predictSteeringAngle(self, image):
            preprocessed = self.__preprocess(image)
            X = np.asarray([preprocessed])
            steering_angle = self.model.predict(X)[0]
            return steering_angle
        def __preprocess(self,image):
            height, _, _ = image.shape
            qheight = int(height/4)
            hheight = int(height/2)
            image = image[qheight:qheight+hheight,:,:] # cropping so only the middle half is visible
            image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
            image = cv2.GaussianBlur(image, (3,3), 0)
            image = cv2.resize(image, (200,66)) # input image size (200,66) Nvidia model
            image = image / 255 # normalizing
            return image
if __name__ == "__main__":
    laneNavigator = LaneNavigator("../../CNN/lane_navigation.h5")
    image_name = "0496_1016_1212.jpg"
    test_image = cv2.imread("../../training_data/black_dot/%s" % (image_name))
    angle = laneNavigator.predictSteeringAngle(test_image)
    print(angle)

