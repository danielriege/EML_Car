from tensorflow.keras.models import load_model

class LaneNavigator:
        def __init__(self, model_path):
            self.model = load_model(model_path)
        def predictSteeringAngle(self, image):
            preprocessed = preprocess(image)
            X = np.asarray([preprocessed])
            steering_angle = model.predict(X)[0]
            return steering_angle
        def __preprocess(image):
            height, _, _ = image.shape
            qheight = int(height/4)
            hheight = int(height/2)
            image = image[qheight:qheight+hheight,:,:] # cropping so only the middle half is visible
            image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
            image = cv2.GaussianBlur(image, (3,3), 0)
            image = cv2.resize(image, (200,66)) # input image size (200,66) Nvidia model
            image = image / 255 # normalizing
            return image
