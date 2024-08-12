import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from tensorflow.keras import layers, models

from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    """# Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")"""
    filepath = os.path.abspath(sys.argv[0] + f"{os.sep}..")

    # Get image arrays and labels for all image files
    images, labels = load_data(filepath) # sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )
    # print(len(images), images[0].shape, len(labels), len(labels[0]))
    # print(images[0], labels[0])

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    """# Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")"""
    prediction = model.predict(x_test)
    print([np.argmax(prediction[i], 0) for i in range(30)])
    print([np.argmax(y_test[i], 0) for i in range(30)])

    # saving a model to a file to be able to reuse the model
    filename = fr"C:\Users\daniil.navodey\Documents\CS50\traffic\model.keras"
    model.save(filename)
    print(f"Model saved to {filename}.")


def load_data(data_dir):
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
    labels = []
    print("Loading data from folders:")
    import tqdm

    for i in tqdm.tqdm(range(NUM_CATEGORIES)):
        # joining the filepath to each folder
        filepath = os.path.abspath(f"traffic/gtsrb/{i}")

        # traversing through all the riles in directory & appending images and labels array with data from the file
        for file in os.listdir(filepath):
            # reading the .ppm file
            image = cv2.imread(os.path.join(filepath, file))

            # converting BGR to RGB, cuz imread module inverses the values
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

            #resizing the image
            image = np.array(cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT), interpolation=cv2.INTER_LINEAR))

            images.append(image)
            labels.append(i)

    return images, labels



def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = models.Sequential([
        # tf.keras.Input((IMG_WIDTH, IMG_HEIGHT, 3)),
        layers.Conv2D(64, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), batch_size=None),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        # layers.Conv2D(64, (2, 2), activation='relu'),
        # layers.Conv2D(64, (3, 3), activation='relu'),
        # layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        # layers.Dropout(0.1),
        layers.Dense(32, activation='relu'),
        layers.Dense(NUM_CATEGORIES, activation="softmax")
        ])
    model.summary()
    model.compile(optimizer='adam',
              loss="categorical_crossentropy",
              metrics=['accuracy'])

    return model



if __name__ == "__main__":
    main()
