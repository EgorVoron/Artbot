import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json
import datetime
import time

labels = ['картина/рисунок', 'гравюра', 'икона', 'картина', 'скульптура']


def model_loader():
    json_file = open('js_18.json', 'r')  # file with model config
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights('model_18feb.h5')
    loaded_model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    return loaded_model


class ClassPredictor:

    def __init__(self):
        self.dim = 150
        self.labels = labels
        self.loaded_model = model_loader()
        self.img = None
        self.time = None

    def process_img(self, inp_img):
        self.time = time.time()
        self.img = inp_img
        plt.imshow(self.img)
        plt.show()
        self.img = self.img.resize((self.dim, self.dim))
        self.img = np.reshape(self.img, (1, self.dim, self.dim, 3))
        return self.img

    def predict(self, img):
        loaded_model = self.loaded_model
        ans = loaded_model.predict(x=img)
        out = labels[np.argmax(ans)]
        time_of_prediction = time.time() - self.time
        print(datetime.datetime.now(), out, time_of_prediction)
        return out
