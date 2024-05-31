from PyQt6 import QtWidgets
from SubTabs import SubTabs
from typing import List

class PlotWidget(QtWidgets.QTabWidget):
    def __init__(self, datacollector):
        self.tabs_index = 0

        super().__init__()
        self.setWindowTitle("Plot Widget")
        self.setMinimumSize(600, 600)
        self.subtabs: List[SubTabs] = []
        self.datacollector = datacollector

    def createNewTab(self, datacollector, fitpage_index):
        #check if the tab is already existing. if its not existing: create it. otherwise: change to the index of the tab
        plot_index = datacollector.get_data_by_fitpage_index(fitpage_index).get_plotpage_index()
        if plot_index == -1:
            datacollector.set_plot_index(fitpage_index, self.tabs_index)
            #create new plotpage
            newTab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(newTab)
            new_subtab = SubTabs(datacollector, fitpage_index)
            layout.addWidget(new_subtab)
            newTab.setLayout(layout)
            #add created plot page to the widget, keep it in the list of tabs to keep track
            self.subtabs.append(new_subtab)
            self.addTab(newTab, "Plot for FitPage "+str(fitpage_index))
            self.setCurrentIndex(self.tabs_index)
            self.tabs_index += 1
        else:
            #show the already existing tab and check if values have changed. if values changed: recalculate
            self.removeTab(plot_index)

            recalculatedTab = QtWidgets.QWidget()
            layout = QtWidgets.QVBoxLayout(recalculatedTab)
            new_subtab = SubTabs(datacollector, fitpage_index)
            layout.addWidget(new_subtab)
            recalculatedTab.setLayout(layout)

            self.subtabs[plot_index] = new_subtab
            self.insertTab(plot_index, recalculatedTab, "Plot for FitPage " + str(fitpage_index))
            self.setCurrentIndex(plot_index)

    def send_data_to_subtab(self, fitpage_from, fitpage_to, subtab_index):
        plottab_index = self.datacollector.get_plotpage_index(fitpage_to)
        self.subtabs[plottab_index].add_dataset_to_subtab(fitpage_from, fitpage_to, subtab_index)
        self.setCurrentIndex(plottab_index)
        self.activateWindow()

    def get_tab_amount(self):
        return self.tabs_index

    def get_existing_subtabs_from_fitpage_index(self, fitpage_index):
        for i in range(len(self.subtabs)):
            if fitpage_index == self.subtabs[i].fitpage_index:
                return self.subtabs[i]

    def get_existing_figures_from_fitpage_index(self, fitpage_index):
        for i in range(len(self.subtabs)):
            if fitpage_index == self.subtabs[i].fitpage_index:
                return self.subtabs[i].figures



