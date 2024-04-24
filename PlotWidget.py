from PyQt6 import QtWidgets
from PyQt6 import QtGui
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.figure

class PlotWidget(QtWidgets.QTabWidget):
    def __init__(self, x_dataset, y_dataset):
        super().__init__()

        newTab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(newTab)

        static_canvas = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 3)))
        layout.addWidget(static_canvas)
        newTab.setLayout(layout)

        static_ax = static_canvas.figure.subplots()
        static_ax.plot(x_dataset, y_dataset)

        self.tabs = []
        self.tabs.append(newTab)
        self.addTab(self.tabs[0], "1")
        self.tabCounter = 1

    def createNewTab(self, x_dataset, y_dataset):
        newTab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(newTab)

        static_canvas = FigureCanvasQTAgg(matplotlib.figure.Figure(figsize=(3, 3)))
        layout.addWidget(static_canvas)
        newTab.setLayout(layout)

        static_ax = static_canvas.figure.subplots()
        static_ax.plot(x_dataset, y_dataset)

        self.tabs.append(newTab)
        self.addTab(self.tabs[self.tabCounter], str(self.tabCounter+1))
        self.tabCounter += 1
