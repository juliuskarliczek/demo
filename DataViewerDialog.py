from DataViewerDialogUI import Ui_DataViewerDialog
from PyQt6 import QtWidgets
from PyQt6 import QtCore

class DataViewerDialog(QtWidgets.QDialog, Ui_DataViewerDialog):

    def __init__(self, fitpage_index_from, datasets, dataviewer):
        super(DataViewerDialog, self).__init__()
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.datasets = datasets
        self.dataviewer = dataviewer
        self.fitpage_index_from = fitpage_index_from
        #show all current datasets beside the one that the data is coming from (the data is already in that page)
        for i in range(len(datasets)):
            if datasets[i][0] != fitpage_index_from:
                self.listToFitpage.addItem("Send to Fitpage "+str(datasets[i][0]))
            else:
                continue

        self.listToFitpage.currentItemChanged.connect(self.cbUpdate)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        if self.listToFitpage.currentItem() != None:
            self.dataviewer.bool_send_to_fitpage = True
            self.dataviewer.send_to_fitpage_index = int(self.listToFitpage.currentItem().text().split()[3])
            self.dataviewer.send_to_subtab_index = self.cbSubtab.currentIndex()
        super().accept()

    def reject(self):
        self.dataviewer.bool_send_to_fitpage = False
        super().reject()

    def cbUpdate(self):
        for i in range(len(self.datasets)):
            if self.datasets[i][0] != self.fitpage_index_from:
                if self.datasets[i][4][0]:
                    self.cbSubtab.addItem("Data")
                if self.datasets[i][4][1]:
                    self.cbSubtab.addItem("Fit")
                if self.datasets[i][4][2]:
                    self.cbSubtab.addItem("Residuals")
            else:
                continue
