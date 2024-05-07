from PyQt6 import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
import matplotlib.figure

from SubTabs import SubTabs

class PlotWidget(QtWidgets.QTabWidget):
    def __init__(self, param_scale, param_radius, show_graphs, int_identifier):
        #for serializing the tabs: e.g. fitpage 5 has tab index 0, because its fitted first
        self.tabs_index = 0
        self.int_identifiers = {}

        super().__init__()
        self.setMinimumSize(600, 600)
        self.tabs = []
        self.createNewTab(param_scale, param_radius, show_graphs, int_identifier)

    def createNewTab(self, param_scale, param_radius, show_graphs, int_identifier):
        #check if the tab is already existing. if its not existing: create it. otherwise: change to the index of the tab
        if not (int_identifier in self.int_identifiers):
            #for serializing the tabs with respect to the fitting pages
            self.int_identifiers.update({int_identifier: self.tabs_index})

            #create new plotpage
            newTab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(newTab)
            layout.addWidget(SubTabs(param_scale, param_radius, show_graphs))
            newTab.setLayout(layout)

            #add created plot page to the widget, keep it in the list of tabs to keep track
            self.tabs.append(newTab)
            self.addTab(self.tabs[self.tabs_index], "Plot for FitPage "+str(int_identifier))
            self.setCurrentIndex(self.tabs_index)
            self.tabs_index += 1
        else:
            #show the already existing tab
            self.setCurrentIndex(self.int_identifiers[int_identifier])
