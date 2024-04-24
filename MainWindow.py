import sys
from PyQt6 import QtWidgets, uic

from MainWindowUI import Ui_MainWindow
from PlotWidget import PlotWidget

from RandomDatasetCreator import createRandomDataset

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Tabbed Plot Demo")

        self.setMinimumSize(500, 500)

        self.cmdCreatePlot.clicked.connect(self.onCreatePlot)

        self.pl = None

    def onCreatePlot(self):
        x_dataset, y_dataset = createRandomDataset()
        if self.pl is None:
            self.pl = PlotWidget(x_dataset, y_dataset)
        else:
            self.pl.createNewTab(x_dataset, y_dataset)

        if not self.pl.isVisible:
            pass
        else:
            self.pl.show()

        self.pl.activateWindow()

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
