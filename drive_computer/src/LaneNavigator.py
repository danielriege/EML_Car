#!/usr/bin/env python3
from tflite_runtime.interpreter import Interpreter, load_delegate
import cv2
import numpy as np
import argparse
import time

class LaneNavigator:
        def __init__(self, model_path):
            # Load TF lite model
            self.interpreter = Interpreter(model_path,
                                        experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
        def predictSteeringAngle(self, image):
            preprocessed = self.__preprocess(image)
            input_data = np.asarray([preprocessed], dtype=np.float32)
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            output_data = (output_data-0.5)*(-1)            
            return np.int((output_data[0]+1.5)*1000)
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
    parser.add_argument('--image', type=str, help='File name of an image in black_dot folder.', required=True)
    args = parser.parse_args()
    imageName = args.image
    laneNavigator = LaneNavigator("../../CNN/black_dot_edgetpu.tflite")
    test_image = cv2.imread("../../training_data/black_dot/%s" % (imageName))
    start = time.time()
    angle = laneNavigator.predictSteeringAngle(test_image)
    print("took: ",(time.time()-start)*1000, "ms")
    print(angle)
if __name__ == "__main__":
    main()
