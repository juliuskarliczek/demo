from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.figure

import RandomDatasetCreator


class SubTabs(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()

        subtab1 = QtWidgets.QWidget()
        layout1 = QtWidgets.QVBoxLayout()
        static_canvas1 = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 3)))
        layout1.addWidget(static_canvas1)
        static_ax1 = static_canvas1.figure.subplots()
        x_dataset, y_dataset = RandomDatasetCreator.createRandomDataset()
        static_ax1.plot(x_dataset, y_dataset)
        subtab1.setLayout(layout1)

        subtab2 = QtWidgets.QWidget()
        layout2 = QtWidgets.QVBoxLayout()
        static_canvas2 = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 3)))
        layout2.addWidget(static_canvas2)
        static_ax2 = static_canvas2.figure.subplots()
        x_dataset, y_dataset = RandomDatasetCreator.createRandomDataset()
        static_ax2.plot(x_dataset, y_dataset)
        subtab2.setLayout(layout2)

        subtab3 = QtWidgets.QWidget()
        layout3 = QtWidgets.QVBoxLayout()
        static_canvas3 = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 3)))
        layout3.addWidget(static_canvas3)
        static_ax3 = static_canvas3.figure.subplots()
        x_dataset, y_dataset = RandomDatasetCreator.createRandomDataset()
        static_ax3.plot(x_dataset, y_dataset)
        subtab3.setLayout(layout3)

        self.subtabs = []
        self.subtabs.append(subtab1)
        self.subtabs.append(subtab2)
        self.subtabs.append(subtab3)

        self.addTab(subtab1, "1")
        self.addTab(subtab2, "2")
        self.addTab(subtab3, "3")


