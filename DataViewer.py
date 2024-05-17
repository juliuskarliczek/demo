from PyQt6 import QtWidgets
from PyQt6 import QtCore
from DataViewerUI import Ui_DataViewer
from DataViewerDialog import DataViewerDialog

class DataViewer(QtWidgets.QWidget, Ui_DataViewer):
    def __init__(self, main_window):
        super(DataViewer, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Data Viewer")

        self.cmdSendToPlotpage.clicked.connect(self.onSendToPlotpage)
        self.cmdClose.clicked.connect(self.onClose)
        self.main_window = main_window
        self.datacollector = self.main_window.datacollector
        self.labelSelectAnItem.hide()

        self.send_to_fitpage_index = None
        self.bool_send_to_fitpage = False
        self.send_to_subtab_index = None

    def update_datasets_from_collector(self, datacollector):
        self.datasetList.clear()
        self.datacollector = datacollector
        datasets = datacollector.datasets
        for i in range(len(datasets)):
            self.datasetList.addItem("Data from Fitpage " + str(datasets[i][0]))

    def onSendToPlotpage(self):
        current_row_index = self.datasetList.currentRow()
        if current_row_index != -1:
            current_item_fitpage_index = int(self.datasetList.currentItem().text().split()[3])
            self.labelSelectAnItem.hide()
            #aufrufen von der funktion vom mainwindow, die das dann zum plotten rüberschickt zu subtabs
            self.dataviewerdialog = DataViewerDialog(current_item_fitpage_index, self.datacollector.get_datasets(), self)
            self.dataviewerdialog.exec()
            if self.send_to_fitpage_index != None and self.bool_send_to_fitpage:
                self.main_window.send_data_to_subtab(current_item_fitpage_index, self.send_to_fitpage_index, self.send_to_subtab_index)
            else:
                #either the close button from the dialog was clicked or only one fitpage exists and so there wont be
                #a fitpage that the data can be sent to
                pass
        else:
            self.labelSelectAnItem.show()

    def onClose(self):
        self.close()

