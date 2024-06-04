from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from SubTabs import SubTabs
from typing import List

class PlotWidget(QTabWidget):
    def __init__(self, datacollector):
        super().__init__()
        self.setWindowTitle("Plot Widget")
        self.setMinimumSize(600, 600)

        self.datacollector = datacollector

    def widget(self, index) -> SubTabs:
        return super().widget(index)

    def createNewTab(self, datacollector, fitpage_index):
        # check if the tab is already existing.
        # if it is not existing: create it. otherwise: recalculate the tab
        plot_index = datacollector.get_data_by_fitpage_index(fitpage_index).get_plotpage_index()
        if plot_index == -1:
            datacollector.set_plot_index(fitpage_index, self.count())
            self.addTab(SubTabs(datacollector, fitpage_index), "Plot for FitPage " + str(fitpage_index))
            self.setCurrentIndex(self.count())
        else:
            self.removeTab(plot_index)
            self.insertTab(plot_index, SubTabs(datacollector, fitpage_index), "Plot for FitPage " + str(fitpage_index))
            self.setCurrentIndex(plot_index)

    def send_data_to_subtab(self, fitpage_from, fitpage_to, subtab_index):
        plottab_index = self.datacollector.get_plotpage_index(fitpage_to)
        self.widget(plottab_index).add_dataset_to_subtab(fitpage_from, fitpage_to, subtab_index)
        self.setCurrentIndex(plottab_index)
        self.activateWindow()

    def get_subtabs(self, fitpage_index):
        for i in range(self.count()):
            if fitpage_index == self.widget(i).fitpage_index:
                return self.widget(i)

    def get_figures(self, fitpage_index):
        for i in range(self.count()):
            if fitpage_index == self.widget(i).fitpage_index:
                return self.widget(i).figures

    def redrawTab(self, tabitem):
        print(tabitem.get_fitpage_index())





