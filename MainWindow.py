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
        self.setFixedSize(700, 560)

        self.cmdPlot.clicked.connect(self.onPlot)
        self.cmdCalculate.clicked.connect(self.onCalculate)
        self.actionNewFitPage.triggered.connect(self.onActionNewFitPage)
        self.fitPageCounter = 1
        self.newFitPage = FitPage(int_identifier=self.fitPageCounter)
        self.fittingTabs.addTab(self.newFitPage, "Fit Page "+str(self.fitPageCounter))

        self.dataviewer = DataViewer(self)
        self.cmdShowDataViewer.clicked.connect(self.dataviewer.onShowDataViewer)

    def onPlot(self):
        fitpage_index = self.fittingTabs.currentWidget().get_int_identifier()
        self.onCalculate()
        self.dataviewer.create_plot(fitpage_index)

    def onCalculate(self):
        fitpage_index = self.fittingTabs.currentWidget().get_int_identifier()
        create_fit = self.fittingTabs.currentWidget().get_checkbox_fit()
        self.dataviewer.update_dataset(self, fitpage_index, create_fit)
        self.dataviewer.update_datasets_from_collector()
        self.dataviewer.show()
        self.dataviewer.activateWindow()
        self.cmdShowDataViewer.setText("Hide Data Viewer")

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
