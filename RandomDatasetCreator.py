import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b, c):
    return a * np.exp(b * x) + c
def createRandomDataset():
    dataset_length = np.random.randint(100)
    a = np.random.random()
    b = np.random.random()

    x_sample = np.linspace(start=0, stop=10, num=500)
    y_sample = np.empty(shape=500)
    for i in range(len(x_sample)):
        y_sample_no_err = a * np.exp(b * x_sample[i])
        err = y_sample_no_err * (np.random.random()-0.5) / 2
        y_sample[i] = a * np.exp(b * x_sample[i]) + err

    parameters_optimal = curve_fit(f=func, xdata=x_sample, ydata=y_sample)
    y_fit = []
    for i in range(len(x_sample)):
        y_fit.append(func(x=x_sample[i], a=parameters_optimal[0][0], b=parameters_optimal[0][1], c=parameters_optimal[0][2]))

    return x_sample, y_sample, y_fit