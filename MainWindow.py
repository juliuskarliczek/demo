import sys
from PyQt6 import QtWidgets

from MainWindowUI import Ui_MainWindow
from PlotWidget import PlotWidget
from FitPage import FitPage
from DataCollector import DataCollector
from DataViewer import DataViewer

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Tabbed Plot Demo")
        self.setMinimumSize(700, 700)

        self.datacollector = DataCollector()
        self.pl = None

        self.cmdCreatePlot.clicked.connect(self.onCreatePlot)
        self.actionNewFitPage.triggered.connect(self.onActionNewFitPage)
        self.fitPageCounter = 1
        self.newFitPage = FitPage(int_identifier=self.fitPageCounter)
        self.fittingTabs.addTab(self.newFitPage, "Fit Page "+str(self.fitPageCounter))
        self.labelWarning.hide()

        self.dataviewer = DataViewer(self)
        self.cmdShowDataViewer.clicked.connect(self.dataviewer.onShowDataViewer)

    def onCreatePlot(self):
        fitpage_index = self.fittingTabs.currentWidget().get_int_identifier()
        self.datacollector.update_dataset(self, fitpage_index)
        show_graphs = self.datacollector.get_show_graphs(fitpage_index)

        if not (show_graphs[0] or show_graphs[1] or show_graphs[2]):
            self.labelWarning.show()
            return
        self.labelWarning.hide()

        self.dataviewer.create_plot(fitpage_index)

    def onActionNewFitPage(self):
        self.fitPageCounter += 1
        self.newFitPage = FitPage(self.fitPageCounter)
        self.fittingTabs.addTab(self.newFitPage, "Fit Page " + str(self.fitPageCounter))
        self.fittingTabs.setCurrentIndex(self.fitPageCounter-1)

    def closeEvent(self, event):
        sys.exit()

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
