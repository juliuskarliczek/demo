from PyQt6 import QtWidgets
from FitPageUI import Ui_fitPageWidget
class FitPage(QtWidgets.QWidget, Ui_fitPageWidget):
    def __init__(self):
        super(FitPage, self).__init__()
        self.setupUi(self)

