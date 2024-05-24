from PyQt6 import QtWidgets
from SubTabs import SubTabs

class PlotWidget(QtWidgets.QTabWidget):
    def __init__(self, data_collector, fitpage_index):
        self.tabs_index = 0

        super().__init__()
        self.setWindowTitle("Plot Widget")
        self.setMinimumSize(600, 600)
        self.tabs = []
        self.subtabs = []
        self.createNewTab(data_collector, fitpage_index)
        self.datacollector = data_collector

    def createNewTab(self, data_collector, fitpage_index):
        #check if the tab is already existing. if its not existing: create it. otherwise: change to the index of the tab
        plot_index = data_collector.get_plot_index(fitpage_index)
        if plot_index == -1:
            data_collector.set_plot_index(fitpage_index, self.tabs_index)
            #create new plotpage
            newTab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(newTab)
            new_subtab = SubTabs(data_collector, fitpage_index)
            layout.addWidget(new_subtab)
            newTab.setLayout(layout)
            #add created plot page to the widget, keep it in the list of tabs to keep track
            self.tabs.append(newTab)
            self.subtabs.append(new_subtab)
            self.addTab(self.tabs[self.tabs_index], "Plot for FitPage "+str(fitpage_index))
            self.setCurrentIndex(self.tabs_index)
            self.tabs_index += 1
        else:
            #show the already existing tab and check if values have changed. if values changed: recalculate
            self.removeTab(plot_index)

            recalculatedTab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(recalculatedTab)
            new_subtab = SubTabs(data_collector, fitpage_index)
            layout.addWidget(new_subtab)
            recalculatedTab.setLayout(layout)

            self.tabs[plot_index] = recalculatedTab
            self.subtabs[plot_index] = new_subtab
            self.insertTab(plot_index, self.tabs[plot_index], "Plot for FitPage "+str(fitpage_index))
            self.setCurrentIndex(plot_index)

    def send_data_to_subtab(self, fitpage_from, fitpage_to, subtab_index):
        plottab_index = self.datacollector.get_plot_index(fitpage_to)
        self.subtabs[plottab_index].add_dataset_to_subtab(fitpage_from, fitpage_to, subtab_index)
        self.setCurrentIndex(plottab_index)
        self.activateWindow()

