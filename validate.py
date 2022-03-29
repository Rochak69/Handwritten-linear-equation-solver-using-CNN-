import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


class Predict():
    def __init__(self) -> None:
        self.model = load_model('./model/17class.h5')
        # self.image = image
        self.class_indices = ['+',
                              '-',
                              '0',
                              '1',
                              '2',
                              '3',
                              '4',
                              '5',
                              '6',
                              '7',
                              '8',
                              '9',
                              '=',
                              'X',
                              'div',
                              'Y',
                              'Z']

    def get_class(self, img):
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x.astype('float32')/255
        z = self.model.predict(x)
        pred = np.argmax(z)
        return self.class_indices[pred]
