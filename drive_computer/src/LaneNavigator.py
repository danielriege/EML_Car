#!/usr/bin/env python3
from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np
import argparse

class LaneNavigator:
        def __init__(self, model_path):
            # Load TF lite model
            self.interpreter = Interpreter(args.model)
            self.interpreter.allocate_tensors()
            self.input_details = interpreter.get_input_details()
            self.output_details = interpreter.get_output_details()
        def predictSteeringAngle(self, image):
            preprocessed = self.__preprocess(image)
            X = np.asarray([preprocessed])
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            output_data = interpreter.get_tensor(self.output_details[0]['index'])
            
            return output_data
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

def main():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--image', help='File name of an image in black_dot folder.', required=True)
    args = parser.parse_args()

    laneNavigator = LaneNavigator("../../CNN/lane_navigation.tflite")
    test_image = cv2.imread("../../training_data/black_dot/%s" % (args.image))
    angle = laneNavigator.predictSteeringAngle(test_image)
    print(angle)
if __name__ == "__main__":
    main()
