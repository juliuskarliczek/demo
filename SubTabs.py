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
            subtab_data = QtWidgets.QWidget()
            layout_data = QtWidgets.QVBoxLayout()
            canvas_data = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 2.5)))
            layout_data.addWidget(canvas_data)
            layout_data.addWidget(NavigationToolbar2QT(canvas_data))
            ax_data = canvas_data.figure.subplots()
            ax_data.plot(x_dataset, y_dataset)
            ax_data.set_xscale('log')
            ax_data.set_yscale('log')
            subtab_data.setLayout(layout_data)
            self.subtabs.append(subtab_data)
            self.addTab(subtab_data, "Data")

        if show_graphs[1]:
            subtab_fit = QtWidgets.QWidget()
            layout_fit = QtWidgets.QVBoxLayout()
            canvas_fit = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 3)))
            layout_fit.addWidget(canvas_fit)
            layout_fit.addWidget(NavigationToolbar2QT(canvas_fit))
            ax_fit = canvas_fit.figure.subplots()
            ax_fit.plot(x_dataset, y_dataset)
            ax_fit.plot(x_dataset, y_fit)
            ax_fit.set_xscale('log')
            ax_fit.set_yscale('log')
            subtab_fit.setLayout(layout_fit)
            self.subtabs.append(subtab_fit)
            self.addTab(subtab_fit, "Fit")

        if show_graphs[2]:
            subtab_residuals = QtWidgets.QWidget()
            layout_residuals = QtWidgets.QVBoxLayout()
            fig_residuals = matplotlib.figure.Figure(figsize=(3, 3))
            canvas_residuals = FigureCanvasQTAgg(fig_residuals)
            layout_residuals.addWidget(canvas_residuals)
            layout_residuals.addWidget(NavigationToolbar2QT(canvas_residuals))
            ax_residuals = canvas_residuals.figure.subplots(2, gridspec_kw={'height_ratios': [3, 1]})
            ax_residuals[0].set_ylabel("fit")
            ax_residuals[0].plot(x_dataset, y_dataset, color='tab:brown')
            ax_residuals[0].plot(x_dataset, y_fit, color='tab:blue')

            ax_residuals[0].set_xscale('log')
            ax_residuals[0].set_yscale('log')

            ax_residuals[1].set_ylabel("residuals")
            ax_residuals[1].set_yscale('log')
            ax_residuals[1].plot(x_dataset, np.subtract(y_dataset, y_fit), color='tab:green')
            subtab_residuals.setLayout(layout_residuals)
            self.subtabs.append(subtab_residuals)
            self.addTab(subtab_residuals, "Residuals")


    def add_dataset_to_subtab(self, from_fitpage_index, to_fitpage_index, which_subtab):
        #from_fitpage is the fitpage that the data originates from
        #to_fitpage is the plotpage for the fitpage thats supposed to display the additional data
        self.removeTab(which_subtab)

        adjustedtab = QtWidgets.QWidget()
        layout_adjusted = QtWidgets.QVBoxLayout()
        fig_adjusted = matplotlib.figure.Figure(figsize=(3, 3))
        canvas_adjusted = FigureCanvasQTAgg(fig_adjusted)
        layout_adjusted.addWidget(canvas_adjusted)
        layout_adjusted.addWidget(NavigationToolbar2QT(canvas_adjusted))
        ax_adjusted = canvas_adjusted.figure.subplots()
        ax_adjusted.set_ylabel("data")

        ax_adjusted.set_xscale('log')
        ax_adjusted.set_yscale('log')

        x_dataset = self.datacollector.get_x_data(from_fitpage_index)
        y_dataset = self.datacollector.get_y_data(from_fitpage_index)
        y_fit = self.datacollector.get_y_fit_data(from_fitpage_index)

        ax_adjusted.plot(x_dataset, y_dataset, color='tab:brown')
        ax_adjusted.plot(x_dataset, y_fit, color='tab:blue')

        adjustedtab.setLayout(layout_adjusted)

        self.insertTab(which_subtab, adjustedtab, "Adjusted Subtab")


    def create_mpl_layout(self):
       pass

