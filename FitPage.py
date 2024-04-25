from PyQt6 import QtWidgets
from FitPageUI import Ui_fitPageWidget


class FitPage(QtWidgets.QWidget, Ui_fitPageWidget):
    def __init__(self, int_identifier):
        super(FitPage, self).__init__()
        self.setupUi(self)

        #fitPageIdentifier keeps track of which number this fitpage is identifier by (it is incremental)
        self.fitPageIdentifier = int_identifier

    def get_int_identifier(self):
        return self.fitPageIdentifier
