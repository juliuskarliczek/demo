import numpy as np

def createRandomDataset():
    dataset_length = np.random.randint(50)

    x_sample = np.random.rand(dataset_length)
    y_sample = np.random.rand(dataset_length)

    return x_sample, y_sample