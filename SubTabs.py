from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
import matplotlib.figure

import RandomDatasetCreator
import numpy as np

class SubTabs(QtWidgets.QTabWidget):
    def __init__(self, data_collector, fitpage_index):
        super().__init__()

        self.datacollector = data_collector
        self.fitpage_index = fitpage_index
        self.subtabs = []
        x_dataset = data_collector.get_x_data(fitpage_index)
        y_dataset = data_collector.get_y_data(fitpage_index)
        y_fit = data_collector.get_y_fit_data(fitpage_index)
        show_graphs = data_collector.get_show_graphs(fitpage_index)

        if show_graphs[0]:
            subtab = self.new_subtab([x_dataset], [y_dataset],
                                     settings={"xscale": "log", "yscale": "log",
                                                "xlabel": "xdata", "ylabel": "ydata", "toolbar": True, "grid": True})
            self.subtabs.append(subtab)
            self.addTab(subtab, "Data")

        if show_graphs[1]:
            subtab = self.new_subtab([x_dataset], [y_dataset, y_fit],
                                     settings={"xscale": "log", "yscale": "log",
                                               "xlabel": "xdata", "ylabel": "ydata", "toolbar": True, "grid": True})
            self.subtabs.append(subtab)
            self.addTab(subtab, "Fit")

        if show_graphs[2]:
            subtab = self.new_subtab([x_dataset], [y_dataset, y_fit],
                                     settings={"xscale": "log", "yscale": "log",
                                               "xlabel": "xdata", "ylabel": "ydata", "toolbar": True,
                                               "residuals": True, "grid": True})
            self.subtabs.append(subtab)
            self.addTab(subtab, "Residuals")


    def add_dataset_to_subtab(self, from_fitpage_index, to_fitpage_index, which_subtab):
        #from_fitpage is the fitpage that the data originates from
        #to_fitpage is the plotpage for the fitpage thats supposed to display the additional data
        self.removeTab(which_subtab)

        x_dataset_from = self.datacollector.get_x_data(from_fitpage_index)
        y_dataset_from = self.datacollector.get_y_data(from_fitpage_index)
        y_fit_from = self.datacollector.get_y_fit_data(from_fitpage_index)

        x_dataset_to = self.datacollector.get_x_data(to_fitpage_index)
        y_dataset_to = self.datacollector.get_y_data(to_fitpage_index)
        y_fit_to = self.datacollector.get_y_fit_data(to_fitpage_index)

        adjustedtab = self.new_subtab([x_dataset_from, x_dataset_from, x_dataset_to, x_dataset_to],
                                      [y_dataset_from, y_fit_from, y_dataset_to, y_fit_to],
                                      settings={"xscale": "log", "yscale": "log",
                                                "xlabel": "xdata", "ylabel": "dataothertab", "toolbar": True,
                                                "grid": True})
        self.insertTab(which_subtab, adjustedtab, "Adjusted Subtab")
        self.setCurrentIndex(which_subtab)

    def new_subtab(self, xdata, ydata, settings):
        # xdata is a list of lists containing the xdata at every position for the certain subplot
        # settings is a dict of e.g. {xlabel: 'foo', ylabel: 'bar', xscale: 'a', yscale: 'b', nrows: int, ncols: int,
        #                               toolbar: True, grid: True}
        residuals_b = False
        subtab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        figure = matplotlib.figure.Figure(figsize=(3, 3))
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
        else:
            ax = canvas.figure.subplots()

        for i in range(len(ydata)):
            if residuals_b:
                if len(xdata) > 1:
                    ax[0].plot(xdata[i], ydata[i])
                else:
                    ax[0].plot(xdata[0], ydata[i])
                ax[1].plot(xdata[0], np.subtract(ydata[1], ydata[0]), color='tab:green')
            else:
                if len(xdata) > 1:
                    ax.plot(xdata[i], ydata[i])
                else:
                    ax.plot(xdata[0], ydata[i])
        if residuals_b:
            if "xlabel" in settings:
                ax[0].set_xlabel(settings["xlabel"])
                ax[1].set_xlabel(settings["xlabel"])
            if "ylabel" in settings:
                ax[0].set_ylabel(settings["ylabel"])
            if "xscale" in settings:
                ax[0].set_xscale(settings["xscale"])
            if "yscale" in settings:
                ax[0].set_yscale(settings["yscale"])
            if "grid" in settings:
                if settings["grid"]:
                    ax[0].grid(True)
                    ax[1].grid(True)
            ax[1].set_xscale("log")
            ax[1].set_yscale("log")
            ax[1].set_ylabel("residuals")
        else:
            if "xlabel" in settings:
                ax.set_xlabel(settings["xlabel"])
            if "ylabel" in settings:
                ax.set_ylabel(settings["ylabel"])
            if "xscale" in settings:
                ax.set_xscale(settings["xscale"])
            if "yscale" in settings:
                ax.set_yscale(settings["yscale"])
            if "grid" in settings:
                if settings["grid"]:
                    ax.grid(True)

        subtab.setLayout(layout)
        return subtab
