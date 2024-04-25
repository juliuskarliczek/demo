from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.figure

import RandomDatasetCreator
import numpy as np

from scipy.optimize import curve_fit


class SubTabs(QtWidgets.QTabWidget):
    def __init__(self, param_a, param_b, show_graphs):
        super().__init__()
        self.subtabs = []
        x_dataset, y_dataset, y_fit = RandomDatasetCreator.createRandomDataset(param_a, param_b)

        if show_graphs[0]:
            subtab_data = QtWidgets.QWidget()
            layout_data = QtWidgets.QVBoxLayout()
            static_canvas_data = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 2.5)))
            layout_data.addWidget(static_canvas_data)
            static_ax_data = static_canvas_data.figure.subplots()
            static_ax_data.plot(x_dataset, y_dataset)
            subtab_data.setLayout(layout_data)
            self.subtabs.append(subtab_data)
            self.addTab(subtab_data, "Data")

        if show_graphs[1]:
            subtab_fit = QtWidgets.QWidget()
            layout_fit = QtWidgets.QVBoxLayout()
            static_canvas_fit = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 3)))
            layout_fit.addWidget(static_canvas_fit)
            static_ax_fit = static_canvas_fit.figure.subplots()
            static_ax_fit.plot(x_dataset, y_dataset)
            static_ax_fit.plot(x_dataset, y_fit)
            subtab_fit.setLayout(layout_fit)
            self.subtabs.append(subtab_fit)
            self.addTab(subtab_fit, "Fit")

        if show_graphs[2]:
            subtab_residuals = QtWidgets.QWidget()
            layout_residuals = QtWidgets.QVBoxLayout()
            fig_residuals = matplotlib.figure.Figure(figsize=(3, 3))
            static_canvas_residuals = FigureCanvasQTAgg(fig_residuals)
            layout_residuals.addWidget(static_canvas_residuals)
            static_ax_residuals = static_canvas_residuals.figure.subplots()
            static_ax_residuals.set_ylabel("fit")
            static_ax_residuals.plot(x_dataset, y_dataset, color='tab:brown')
            static_ax_residuals.plot(x_dataset, y_fit, color='tab:blue')

            static_ax_lin_scale = static_ax_residuals.twinx()
            static_ax_lin_scale.set_ylabel("residuals")
            static_ax_lin_scale.plot(x_dataset, np.subtract(y_dataset, y_fit), color='tab:gray', alpha=0.3)
            #fig_residuals.tight_layout()
            subtab_residuals.setLayout(layout_residuals)
            self.subtabs.append(subtab_residuals)
            self.addTab(subtab_residuals, "Residuals")
