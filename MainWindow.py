import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt

from MainWindowUI import Ui_MainWindow
from PlotWidget import PlotWidget

from RandomDatasetCreator import createRandomDataset

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Tabbed Plot Demo")

        self.setMinimumSize(700, 700)

        self.cmdCreatePlot.clicked.connect(self.onCreatePlot)
        self.labelWarning.hide()

        self.pl = None

    def onCreatePlot(self):
        show_graphs = (self.cbData.isChecked(), self.cbFit.isChecked(), self.cbResiduals.isChecked())
        if not (show_graphs[0] or show_graphs[1] or show_graphs[2]):
            self.labelWarning.show()
            return
        self.labelWarning.hide()
        if self.pl is None:
            self.pl = PlotWidget(show_graphs)
        else:
            self.pl.createNewTab(show_graphs)

        if not self.pl.isVisible:
            pass
        else:
            self.pl.show()

        self.pl.activateWindow()

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
