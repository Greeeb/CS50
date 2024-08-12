import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow.keras import layers, models
from matplotlib import pyplot as plt
import traffic
import tqdm        


IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43

def main():
    # joining the filepath to each folder
    filepath = os.path.abspath(r"traffic/test")
    images = load_data(filepath=filepath)
    print(np.array(images).shape)
    
    model = models.load_model(os.path.abspath(r"traffic/model_9635.keras"))
    
    predictions = model.predict(images, batch_size=31)
    print(np.argmax(predictions[0]))
    
    
    
def load_data(filepath):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    print("Loading data from folder:")

    # traversing through all the riles in directory & appending images and labels array with data from the file
    for file in tqdm.tqdm(os.listdir(filepath)):
        # reading the .ppm file
        image = cv2.imread(os.path.join(filepath, file))

        # converting BGR to RGB, cuz imread module inverses the values
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        #resizing the image
        image = np.array(cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_LINEAR))
        plt.imshow(image)
        # plt.show()
        images.append(image)

    return images



if __name__ == "__main__":
    main()