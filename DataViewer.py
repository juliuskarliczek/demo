from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem
from DataViewerUI import Ui_DataViewer
from PlotWidget import PlotWidget
from DataTreeWidget import DataTreeWidget
from PlotTreeWidget import PlotTreeWidget
from DataCollector import DataCollector
from DataTreeItems import PlotPageItem, DataItem
from PlotTreeItems import TabItem, SubTabItem, PlotItem, PlottableItem


class DataViewer(QtWidgets.QWidget, Ui_DataViewer):
    def __init__(self, main_window):
        super(DataViewer, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Data Viewer")
        self.setMinimumSize(400, 500)

        self.main_window = main_window
        self.datacollector = DataCollector()

        self.dataTreeWidget = DataTreeWidget(self, self.datacollector)
        self.plotTreeWidget = PlotTreeWidget(self)
        self.labelSelectAnItem.hide()

        self.cmdSendToPlotpage.clicked.connect(self.onSendToPlotpage)
        self.cmdClose.clicked.connect(self.onShowDataViewer)
        self.dataTreeWidget.currentItemChanged.connect(self.updateComboboxes)
        self.cmdRedrawCurrentItem.clicked.connect(self.redrawCurrentItem)

        self.plot_widget = PlotWidget(self.datacollector)
        self.data_origin_fitpage_index = None

    def create_plot(self, fitpage_index):
        self.plot_widget.createNewTab(self.datacollector, fitpage_index)
        if not self.plot_widget.isVisible:
            pass
        else:
            self.plot_widget.show()
        self.update_plot_tree()
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
            self.data_origin_fitpage_index = int(self.datacollector.get_dataset_by_id(data_id).get_fitpage_index())

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

    def update_plot_tree(self):
        self.plotTreeWidget.blockSignals(True)
        self.plotTreeWidget.clear()
        self.plotTreeWidget.blockSignals(False)

        # iterate through all tabs from the plot widget
        for i in range(self.plot_widget.count()):
            tab_name = self.plot_widget.tabText(i)

            fitpage_index = self.plot_widget.widget(i).get_fitpage_index()
            tab_item = TabItem(self.plotTreeWidget, [tab_name], fitpage_index)
            tab_item.setData(0, 1, tab_item)

            subtab = self.plot_widget.get_subtabs(fitpage_index)
            figures = self.plot_widget.get_figures(fitpage_index)
            # iterate through all the subplots of one tab
            for j in range(subtab.count()):

                subtab_item = SubTabItem(tab_item, [subtab.tabText(j)], fitpage_index, j)
                subtab_item.setData(0, 1, subtab_item)

                # iterate through all the subplots/axes of one subtab
                ax = subtab.figures[j].get_axes()
                for k in range(len(ax)):
                    plot_item = PlotItem(subtab_item, [ax[k].get_title()], fitpage_index, j, k)
                    plot_item.setData(0, 1, plot_item)

            #subtab.figures[0].get_axes()[0].plot(np.linspace(1, 100, 500),
                                                 #np.linspace(1, 100, 500))


    def redrawCurrentItem(self):
        if self.plotTreeWidget.currentItem() is not None:
            current_data = self.plotTreeWidget.currentItem().data(0, 1)
            if current_data is not None:
                if isinstance(current_data, TabItem):
                    self.plot_widget.redrawTab(current_data)
                elif isinstance(current_data, SubTabItem):
                    pass # redraw subtab
                    #self.plot_widget.redrawSubtab(current_data)
                elif isinstance(current_data, PlotItem):
                    pass # redraw plot
                    #self.plot_widget.redrawPlot(current_data)
                else:
                    pass # redrawing makes no sense for the plottable item, because the whole plot has to be replotted
