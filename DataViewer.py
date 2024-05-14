from PyQt6 import QtWidgets
from DataViewerUI import Ui_DataViewer


class DataViewer(QtWidgets.QWidget, Ui_DataViewer):
    def __init__(self):
        super(DataViewer, self).__init__()
        self.setupUi(self)