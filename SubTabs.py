from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from typing import List
import matplotlib.figure

import RandomDatasetCreator
import numpy as np

class SubTabs(QtWidgets.QTabWidget):
    def __init__(self, datacollector, fitpage_index):
        super().__init__()

        self.datacollector = datacollector
        self.fitpage_index = fitpage_index
        self.subtabs: List[QtWidgets.QWidget] = []
        self.figures: List[matplotlib.figure] = []
        x_dataset = datacollector.get_x_data(fitpage_index)
        y_dataset = datacollector.get_y_data(fitpage_index)

        subtab, figure = self.new_subtab([x_dataset], [y_dataset],
                                 settings={"xscale": "log", "yscale": "log",
                                           "xlabel": "xdata", "ylabel": "ydata", "toolbar": True,
                                           "grid": True, "title": "data plot"})
        self.subtabs.append(subtab)
        self.figures.append(figure)
        self.addTab(subtab, "Data")

        if datacollector.get_data_by_fitpage_index(fitpage_index).has_y_fit():
            y_fit = datacollector.get_y_fit_data(fitpage_index)
            subtab_fit, figure_fit = self.new_subtab([x_dataset], [y_dataset, y_fit],
                                         settings={"xscale": "log", "yscale": "log",
                                                   "xlabel": "xdata", "ylabel": "ydata", "toolbar": True,
                                                   "grid": True, "title": "fit plot"})
            self.subtabs.append(subtab_fit)
            self.figures.append(figure_fit)
            self.addTab(subtab_fit, "Fit")

            subtab_res, figure_res = self.new_subtab([x_dataset], [y_dataset, y_fit],
                                         settings={"xscale": "log", "yscale": "log",
                                                   "xlabel": "xdata", "ylabel": "ydata", "toolbar": True,
                                                   "residuals": True,
                                                   "grid": True, "title": "fit plot"})
            self.subtabs.append(subtab_res)
            self.figures.append(figure_res)
            self.addTab(subtab_res, "Residuals")

    def add_dataset_to_subtab(self, from_fitpage_index, to_fitpage_index, which_subtab):
        #from_fitpage is the fitpage that the data originates from
        #to_fitpage is the plotpage for the fitpage thats supposed to display the additional data
        old_subtab_name = self.tabText(which_subtab)
        self.removeTab(which_subtab)

        x_dataset_from = self.datacollector.get_x_data(from_fitpage_index)
        y_dataset_from = self.datacollector.get_y_data(from_fitpage_index)

        x_dataset_to = self.datacollector.get_x_data(to_fitpage_index)
        y_dataset_to = self.datacollector.get_y_data(to_fitpage_index)

        adjustedtab = self.new_subtab([x_dataset_from, x_dataset_to],
                                      [y_dataset_from, y_dataset_to],
                                      settings={"xscale": "log", "yscale": "log",
                                                "xlabel": "xdata", "ylabel": "dataothertab", "toolbar": True,
                                                "grid": True})

        final_subtab_label = old_subtab_name + "FP " + str(from_fitpage_index) + "+Data FP " + str(to_fitpage_index)
        self.insertTab(which_subtab, adjustedtab, final_subtab_label)
        self.setCurrentIndex(which_subtab)

    def new_subtab(self, xdata, ydata, settings):
        # xdata is a list of lists containing the xdata at every position for the certain subplot
        # settings is a dict of e.g. {xlabel: 'foo', ylabel: 'bar', xscale: 'a', yscale: 'b', nrows: int, ncols: int,
        #                               toolbar: True, grid: True, title: 'title'}
        residuals_b = False
        subtab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        figure = matplotlib.figure.Figure(figsize=(5, 5))
        canvas = FigureCanvasQTAgg(figure)
        layout.addWidget(canvas)
        if "toolbar" in settings:
            if settings["toolbar"]:
                layout.addWidget(NavigationToolbar2QT(canvas))
        if "residuals" in settings:
            if settings["residuals"]:
                residuals_b = True
                ax = canvas.figure.subplots(2, gridspec_kw={'height_ratios': [3, 1]})
            else:
                ax = canvas.figure.subplots()
                ax = [ax]
        else:
            ax = canvas.figure.subplots()
            ax = [ax]

        for i in range(len(ydata)):
            if len(xdata) > 1:
                ax[0].plot(xdata[i], ydata[i])
            else:
                ax[0].plot(xdata[0], ydata[i])
        if residuals_b:
            ax[1].plot(xdata[0], np.subtract(ydata[1], ydata[0]), color='tab:green')
            ax[1].set_title("residuals")
            ax[1].grid(True)
            ax[1].set_xscale("log")
            ax[1].set_yscale("linear")
            ax[1].set_xlabel(settings["xlabel"])
            #ax[1].set_ylabel()

        if "title" in settings:
            ax[0].set_title(settings["title"])
        if "xlabel" in settings:
            ax[0].set_xlabel(settings["xlabel"])
        if "ylabel" in settings:
            ax[0].set_ylabel(settings["ylabel"])
        if "xscale" in settings:
            ax[0].set_xscale(settings["xscale"])
        if "yscale" in settings:
            ax[0].set_yscale(settings["yscale"])
        if "grid" in settings:
            if settings["grid"]:
                ax[0].grid(True)

        figure.tight_layout()
        subtab.setLayout(layout)
        return subtab, figure

    def get_fitpage_index(self):
        return self.fitpage_index
