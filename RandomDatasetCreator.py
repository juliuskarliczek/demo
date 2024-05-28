import numpy as np
from scipy.optimize import curve_fit
from scipy import integrate
from scipy import special


class DatasetCreator:
    def __init__(self):
        self.combobox_index = -1

    def func(self, q, scale, radius, height):
        if self.combobox_index == 0:
            volume = 4 / 3 * np.pi * radius**3
            return scale / volume * (3*volume*(np.sin(q*radius)-q*radius*np.cos(q*radius)) / (q*radius)**3)**2
        elif self.combobox_index == 1:
            volume = height * np.pi * radius**2
            return 4 * scale * volume * (special.jv(1, q*radius))**2 / (q*radius)**2

    def createRandomDataset(self, scale, radius, height, combobox_index, fit=False):
        self.combobox_index = combobox_index
        length = 4999
        q_sample = np.linspace(start=1, stop=100, num=length)
        y_sample = np.empty(shape=length)
        for i in range(len(q_sample)):
            y_sample_no_err = self.func(q_sample[i], scale, radius, height)
            err = y_sample_no_err * (np.random.random()-0.5) / 2
            y_sample[i] = y_sample_no_err + err

        y_fit = []
        if fit:
            parameters_optimal = curve_fit(f=self.func, xdata=q_sample, ydata=y_sample)
            for i in range(len(q_sample)):
                y_fit.append(self.func(q_sample[i], parameters_optimal[0][0], parameters_optimal[0][1], parameters_optimal[0][2]))

        return q_sample, y_sample, y_fit

