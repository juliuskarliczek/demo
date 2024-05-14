from PyQt6 import QtWidgets
from SubTabs import SubTabs

class PlotWidget(QtWidgets.QTabWidget):
    def __init__(self, data_collector, fitpage_index):
        self.tabs_index = 0

        super().__init__()
        self.setMinimumSize(600, 600)
        self.tabs = []
        self.createNewTab(data_collector, fitpage_index)

    def createNewTab(self, data_collector, fitpage_index):
        #check if the tab is already existing. if its not existing: create it. otherwise: change to the index of the tab
        plot_index = data_collector.get_plot_index(fitpage_index)
        if plot_index == -1:
            data_collector.set_plot_index(fitpage_index, self.tabs_index)
            #create new plotpage
            newTab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(newTab)
            layout.addWidget(SubTabs(data_collector, fitpage_index))
            newTab.setLayout(layout)
            #add created plot page to the widget, keep it in the list of tabs to keep track
            self.tabs.append(newTab)
            self.addTab(self.tabs[self.tabs_index], "Plot for FitPage "+str(fitpage_index))
            self.setCurrentIndex(self.tabs_index)
            self.tabs_index += 1
        else:
            #show the already existing tab and check if values have changed. if values changed: recalculate
            self.removeTab(plot_index)

            recalculatedTab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(recalculatedTab)
            layout.addWidget(SubTabs(data_collector, fitpage_index))
            recalculatedTab.setLayout(layout)

            self.tabs[plot_index] = recalculatedTab
            self.insertTab(plot_index, self.tabs[plot_index], "Plot for FitPage "+str(fitpage_index))
            self.setCurrentIndex(plot_index)

