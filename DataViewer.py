from PyQt6 import QtWidgets
from DataViewerUI import Ui_DataViewer


class DataViewer(QtWidgets.QWidget, Ui_DataViewer):
    def __init__(self, main_window):
        super(DataViewer, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Data Viewer")

        self.cmdSendToPlotpage.clicked.connect(self.onSendToPlotpage)
        self.main_window = main_window
        self.datacollector = self.main_window.datacollector

    def update_datasets_from_collector(self, datacollector):
        self.datasetList.clear()
        self.datacollector = datacollector
        datasets = datacollector.datasets
        for i in range(len(datasets)):
            self.datasetList.addItem("Data from Fitpage " + str(datasets[i][0]))

    def onSendToPlotpage(self):
        dataset = self.datasetList.currentRow()
        current_item = self.datasetList.currentItem()

        print(dataset)
        print(current_item.text().split()[3])
