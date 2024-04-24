from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.figure

from SubTabs import SubTabs

class PlotWidget(QtWidgets.QTabWidget):
    def __init__(self, show_graphs):
        super().__init__()
        self.setMinimumSize(600,600)
        newTab = QtWidgets.QWidget()

        layout = QtWidgets.QVBoxLayout(newTab)
        layout.addWidget(SubTabs(show_graphs))
        newTab.setLayout(layout)

        self.tabs = []
        self.tabs.append(newTab)
        self.addTab(self.tabs[0], "1")
        self.tabCounter = 1

    def createNewTab(self, show_graphs):
        newTab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(newTab)
        layout.addWidget(SubTabs(show_graphs))
        newTab.setLayout(layout)

        self.tabs.append(newTab)
        self.addTab(self.tabs[self.tabCounter], str(self.tabCounter+1))
        self.setCurrentIndex(self.tabCounter)
        self.tabCounter += 1
