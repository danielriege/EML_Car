#!/usr/bin/env python3
from tflite_runtime.interpreter import Interpreter, load_delegate
import cv2
import numpy as np
import argparse
import time

#for grad cam
import tensorflow as tf
from vis.visualization import visualize_cam, overlay
import matplotlib.cm as cm
from matplotlib import pyplot as plt

class LaneNavigator:
        def __init__(self, model_path):
            # Load TF lite model
            print("[LaneNavigator] loading machine learning model")
            self.interpreter = Interpreter(model_path,
                                        experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
            self.model = tf.keras.models.load_model('../models/street.h5')
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            print("[LaneNavigator] model loaded successfully.")
        def predictSteeringAngle(self, image):
            preprocessed = self.__preprocess(image)
            input_data = np.asarray([preprocessed], dtype=np.float32)
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
           # output_data = (output_data-0.5)*(-1)
            return np.int((output_data[0]+1.0)*1000)
        def visualizeActivationMap(self, image):
            preprocessed = self.__preprocess(image)
            heatmap = visualize_cam(self.model, layer_idx=-9, filter_indices=0, penultimate_layer_idx=-10,
                            seed_input=preprocessed, grad_modifier="small_values")
            #jet_heatmap = cm.jet(heatmap)[..., :3]
            return heatmap
        def __preprocess(self,image):
            height, _, _ = image.shape
            qheight = int(height/4)
            hheight = int(height/2)
            image = image[-hheight:,:,:] # cropping so only the middle half is visible
            image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
            image = cv2.GaussianBlur(image, (3,3), 0)
            image = cv2.resize(image, (200,66)) # input image size (200,66) Nvidia model
            image = image / 255 # normalizing
            return image

def test():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--image', type=str, help='Image path to test.', required=True)
    args = parser.parse_args()
    imagePath = args.image
    laneNavigator = LaneNavigator("../models/street_edgetpu.tflite")
    test_image = cv2.imread(imagePath)
    start = time.time()
    angle = laneNavigator.predictSteeringAngle(test_image)
    print("took: ",(time.time()-start)*1000, "ms")
    print(angle)
    start = time.time()
    heatmap = laneNavigator.visualizeActivationMap(test_image)
    print("vis took: ",(time.time()-start)*1000, "ms")
    plt.imshow(heatmap)
    plt.show()
if __name__ == "__main__":
    test()
