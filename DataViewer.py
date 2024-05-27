from PyQt6 import QtWidgets
from PyQt6 import QtCore
from DataViewerUI import Ui_DataViewer
from PlotWidget import PlotWidget
from DataTreeWidget import DataTreeWidget


class DataViewer(QtWidgets.QWidget, Ui_DataViewer):
    def __init__(self, main_window):
        super(DataViewer, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Data Viewer")

        self.dataTreeWidget = DataTreeWidget(self)

        self.cmdSendToPlotpage.clicked.connect(self.onSendToPlotpage)
        self.cmdClose.clicked.connect(self.onShowDataViewer)
        self.dataTreeWidget.currentItemChanged.connect(self.updateComboboxes)

        self.main_window = main_window
        self.datacollector = self.main_window.datacollector
        self.labelSelectAnItem.hide()
        self.data_origin_fitpage_index = None

        self.plot_widget = None

    def create_plot(self, fitpage_index):
        if self.plot_widget is None:
            self.plot_widget = PlotWidget(self.datacollector, fitpage_index)
        else:
            self.plot_widget.createNewTab(self.datacollector, fitpage_index)

        if not self.plot_widget.isVisible:
            pass
        else:
            self.plot_widget.show()

        self.plot_widget.activateWindow()

    def update_datasets_from_collector(self):
        # block signals to prevent currentItemChanged to be called. otherwise the program crashes, because it tries
        # to access the current item.
        self.dataTreeWidget.blockSignals(True)
        self.dataTreeWidget.clear()
        self.dataTreeWidget.blockSignals(False)

        datasets = self.datacollector.datasets
        for i in range(len(datasets)):
            name = "Data from Fitpage " + str(datasets[i][0])
            item = QtWidgets.QTreeWidgetItem(self.dataTreeWidget, [name])

    def onSendToPlotpage(self):
        current_row_item = self.dataTreeWidget.currentItem()
        if current_row_item is not None:
            self.labelSelectAnItem.hide()
            target_fitpage_index = None
            subtab_index = None
            # calling the function to send to a subplot from the main window, this function is supposed to be moved to this class instead
            if self.comboBoxTargetFitpage.currentIndex() != -1:
                target_fitpage_index = int(self.comboBoxTargetFitpage.currentText())
            if self.comboBoxTargetSubtab.currentIndex() != -1:
                subtab_index = int(self.comboBoxTargetSubtab.currentIndex())

            if target_fitpage_index is not None:
                if self.plot_widget is not None:
                    self.plot_widget.send_data_to_subtab(self.data_origin_fitpage_index, target_fitpage_index, subtab_index)
                else:
                    pass
            else:
                # either the close button from the dialog was clicked or only one fitpage exists and so there won't be
                # a fitpage that the data can be sent to
                pass
        else:
            # show warning label if no item is selected
            self.labelSelectAnItem.show()

    def updateComboboxes(self):
        self.data_origin_fitpage_index = int(self.dataTreeWidget.currentItem().text(0).split()[3])

        self.comboBoxTargetFitpage.clear()
        self.comboBoxTargetSubtab.clear()

        for i in range(len(self.datacollector.datasets)):
            if self.datacollector.datasets[i][0] != self.data_origin_fitpage_index:
                # target fitpage combobox updating
                self.comboBoxTargetFitpage.addItem(str(self.datacollector.datasets[i][0]))
                # subtabs combobox updating
                if self.datacollector.datasets[i][4][0]:
                    self.comboBoxTargetSubtab.addItem("Data")
                if self.datacollector.datasets[i][4][1]:
                    self.comboBoxTargetSubtab.addItem("Fit")
                if self.datacollector.datasets[i][4][2]:
                    self.comboBoxTargetSubtab.addItem("Residuals")
            else:
                continue

    def onShowDataViewer(self):
        if self.isVisible():
            self.hide()
            self.main_window.cmdShowDataViewer.setText("Show Data Viewer")
            #self.datasetList.setCurrentRow(0)
        else:
            print("ok3")
            self.update_datasets_from_collector()
            print("ok4")
            self.show()
            self.main_window.cmdShowDataViewer.setText("Hide Data Viewer")
            #self.datasetList.setCurrentRow(0)
