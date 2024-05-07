import numpy as np
from scipy.optimize import curve_fit


def func(q, scale, radius):
    volume = 4 / 3 * np.pi * radius**3
    return scale / volume * (3*volume*(np.sin(q*radius)-q*radius*np.cos(q*radius)) / (q*radius)**3)**2


def createRandomDataset(scale, radius):

    length = 4999
    q_sample = np.linspace(start=1, stop=100, num=length)
    y_sample = np.empty(shape=length)
    for i in range(len(q_sample)):
        y_sample_no_err = func(q_sample[i], scale, radius)
        err = y_sample_no_err * (np.random.random()-0.5) / 2
        y_sample[i] = y_sample_no_err + err

    parameters_optimal = curve_fit(f=func, xdata=q_sample, ydata=y_sample)
    y_fit = []
    for i in range(len(q_sample)):
        y_fit.append(func(q=q_sample[i], scale=parameters_optimal[0][0], radius=parameters_optimal[0][1]))

    return q_sample, y_sample, y_fit
