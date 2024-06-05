from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem
from DataViewerUI import Ui_DataViewer
from PlotWidget import PlotWidget
from DataTreeWidget import DataTreeWidget
from PlotTreeWidget import PlotTreeWidget
from DataCollector import DataCollector
from DataTreeItems import PlotPageItem, DataItem
from PlotTreeItems import TabItem, SubTabItem, PlotItem, PlottableItem

from time import sleep


class DataViewer(QtWidgets.QWidget, Ui_DataViewer):
    def __init__(self, main_window):
        super(DataViewer, self).__init__()
        self.setupUi(self)

        self.main_window = main_window
        self.datacollector = DataCollector()

        self.dataTreeWidget = DataTreeWidget(self, self.datacollector)
        self.plotTreeWidget = PlotTreeWidget(self)
        self.labelSelectAnItem.hide()

        self.cmdSendToPlotpage.clicked.connect(self.onSendToPlotpage)
        self.cmdClose.clicked.connect(self.onShowDataViewer)
        self.dataTreeWidget.currentItemChanged.connect(self.updateComboboxes)
        self.plotTreeWidget.dropSignal.connect(self.redrawAll)

        self.plot_widget = PlotWidget(self.datacollector)
        self.data_origin_fitpage_index = None

    def create_plot(self, fitpage_index):
        self.update_plot_tree(fitpage_index)
        self.plot_widget.show()
        self.plot_widget.activateWindow()

    def update_datasets_from_collector(self):
        # block signals to prevent currentItemChanged to be called. otherwise the program crashes, because it tries
        # to access the current item.
        self.dataTreeWidget.blockSignals(True)
        self.dataTreeWidget.clear()
        self.dataTreeWidget.blockSignals(False)

        datasets = self.datacollector.get_datasets()
        for i in range(len(datasets)):
            fitpage_index = datasets[i].get_fitpage_index()
            name = "Data from Fitpage " + str(fitpage_index)
            data_id = datasets[i].get_data_id()
            item = PlotPageItem(self.dataTreeWidget, [name], fitpage_index, data_id)
            item.setData(0, 1, item)
            subitem_data = DataItem(item, ["Data"], fitpage_index, data_id, 1)
            subitem_data.setData(0, 1, subitem_data)
            if datasets[i].has_y_fit():
                subitem_fit = DataItem(item, ["Fit"], fitpage_index, data_id, 2)
                subitem_fit.setData(0, 1, subitem_fit)

        self.dataTreeWidget.expandAll()

    def onSendToPlotpage(self):
        current_row_item = self.dataTreeWidget.currentItem()
        # check if any row is selected
        if current_row_item is not None:
            self.labelSelectAnItem.hide()

            target_fitpage_index = None
            subtab_index = None
            # check if there is a selection in the comboboxes. cant get the text otherwise
            if self.comboBoxTargetFitpage.currentIndex() != -1:
                target_fitpage_index = int(self.comboBoxTargetFitpage.currentText())
            if self.comboBoxTargetSubtab.currentIndex() != -1:
                subtab_index = int(self.comboBoxTargetSubtab.currentIndex())

            # check if a target fitpage is selected in the the combobox
            if target_fitpage_index is not None:

                #check if both fitpages already exist. if only calculate button was used,
                # this is not necessarily the case. create them if they are not created yet.
                if self.plot_widget.widget(target_fitpage_index) is not None:
                    if self.plot_widget.widget(self.data_origin_fitpage_index) is not None:
                        self.plot_widget.send_data_to_subtab(self.data_origin_fitpage_index, target_fitpage_index, subtab_index)
                    else:
                        self.create_plot(self.data_origin_fitpage_index)
                        self.plot_widget.send_data_to_subtab(self.data_origin_fitpage_index, target_fitpage_index, subtab_index)
                else:
                    self.create_plot(target_fitpage_index)
                    self.plot_widget.send_data_to_subtab(self.data_origin_fitpage_index, target_fitpage_index,
                                                         subtab_index)

                self.plot_widget.activateWindow()

        else:
            # show warning label if no item is selected
            self.labelSelectAnItem.show()

    def updateComboboxes(self):
        # clear the comboboxes so that for data and fit subitems no data can be sent
        self.comboBoxTargetFitpage.clear()
        self.comboBoxTargetSubtab.clear()

        # check if a toplevel item is selected
        if isinstance(self.dataTreeWidget.currentItem().data(0, 1), PlotPageItem):
            data_id = self.dataTreeWidget.currentItem().data(0, 1).get_data_id()
            self.data_origin_fitpage_index = int(self.datacollector.get_data_id(data_id).get_fitpage_index())

            # iterate through datasets and get information from tabs and subtabs
            # for every tab besides the already selected one
            for i in range(len(self.datacollector.datasets)):
                if self.datacollector.datasets[i].get_fitpage_index() != self.data_origin_fitpage_index:
                    # target fitpage combobox updating
                    self.comboBoxTargetFitpage.addItem(str(self.datacollector.datasets[i].get_fitpage_index()))
                    # subtabs combobox updating
                    self.comboBoxTargetSubtab.addItem("Data")
                    if self.datacollector.datasets[i].has_y_fit():
                        self.comboBoxTargetSubtab.addItem("Fit")
                        self.comboBoxTargetSubtab.addItem("Residuals")
                else:
                    continue

    def onShowDataViewer(self):
        if self.isVisible():
            self.hide()
            self.main_window.cmdShowDataViewer.setText("Show Data Viewer")
        else:
            self.update_datasets_from_collector()
            self.show()
            self.main_window.cmdShowDataViewer.setText("Hide Data Viewer")

    def update_dataset(self, main_window, fitpage_index, create_fit):
        self.datacollector.update_dataset(main_window, fitpage_index, create_fit)

    def update_plot_tree(self, fitpage_index):
        # check if an item for the fitpage index already exists
        # if one is found - remove from tree
        for i in range(self.plotTreeWidget.topLevelItemCount()):
            if fitpage_index == self.plotTreeWidget.topLevelItem(i).data(0, 1).get_fitpage_index():
                print(f"found existing item {i}")
                self.plotTreeWidget.takeTopLevelItem(i)

        #add tab
        tab_name = "Plot for Fitpage " + str(fitpage_index)
        tab_item = TabItem(self.plotTreeWidget, [tab_name], fitpage_index)
        tab_item.setData(0, 1, tab_item)

        #add data child and corresponding plot children in every case
        subtab_data = SubTabItem(tab_item, ["Data"], fitpage_index, 0)
        subplot_data = PlotItem(subtab_data, ["Data Plot"], fitpage_index, 0, 0)
        plottable_data = PlottableItem(subplot_data, ["Plottable Data"],
                                       self.datacollector.get_data_fp(fitpage_index).get_data_id(), 1)
        #add fit and residuals in case it was generated
        if self.datacollector.get_data_fp(fitpage_index).has_y_fit():
            subtab_fit = SubTabItem(tab_item, ["Fit"], fitpage_index, 1)
            subplot_fit = PlotItem(subtab_fit, ["Fit Plot"], fitpage_index, 1, 0)
            plottable_fit_data = PlottableItem(subplot_fit, ["Plottable Fit Data"],
                                               self.datacollector.get_data_fp(fitpage_index).get_data_id(), 1)
            plottable_fit_fit = PlottableItem(subplot_fit, ["Plottable Fit Fit"],
                                          self.datacollector.get_data_fp(fitpage_index).get_data_id(), 2)

            subtab_res = SubTabItem(tab_item, ["Residuals"], fitpage_index, 2)
            subplot_res_fit = PlotItem(subtab_res, ["Fit Plot"], fitpage_index, 2, 0)
            plottable_res_data = PlottableItem(subplot_res_fit, ["Plottable Res Data"],
                                               self.datacollector.get_data_fp(fitpage_index).get_data_id(), 1)
            plottable_res_fit = PlottableItem(subplot_res_fit, ["Plottable Res Fit"],
                                               self.datacollector.get_data_fp(fitpage_index).get_data_id(), 2)
            subplot_res = PlotItem(subtab_res, ["Residuals Plot"], fitpage_index, 2, 1)
            plottable_res = PlottableItem(subplot_res, ["Plottable Residuals"],
                                          self.datacollector.get_data_fp(fitpage_index).get_data_id(), 3)
        self.plotTreeWidget.expandAll()
        self.redrawAll()

    def redrawAll(self):
        if self.plotTreeWidget.topLevelItemCount() != 0:
            for i in range(self.plotTreeWidget.topLevelItemCount()):
                self.plot_widget.redrawTab(self.plotTreeWidget.topLevelItem(i))

