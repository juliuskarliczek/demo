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

        self.cmdCreatePlot.clicked.connect(self.onCreatePlot)
        self.cmdShowDataViewer.clicked.connect(self.onShowDataViewer)
        self.actionNewFitPage.triggered.connect(self.onActionNewFitPage)
        self.fitPageCounter = 1
        self.newFitPage = FitPage(int_identifier=self.fitPageCounter)
        self.fittingTabs.addTab(self.newFitPage, "Fit Page "+str(self.fitPageCounter))
        self.labelWarning.hide()

        self.datacollector = DataCollector()
        self.dataviewer = DataViewer(self)
        self.pl = None


    def onCreatePlot(self):
        fitpage_index = self.fittingTabs.currentWidget().get_int_identifier()
        self.datacollector.update_dataset(self, fitpage_index)
        show_graphs = self.datacollector.get_show_graphs(fitpage_index)

        print(self.datacollector.datasets[0][2][50])
        if not (show_graphs[0] or show_graphs[1] or show_graphs[2]):
            self.labelWarning.show()
            return
        self.labelWarning.hide()

        if self.pl is None:
            self.pl = PlotWidget(self.datacollector, fitpage_index)
        else:
            self.pl.createNewTab(self.datacollector, fitpage_index)

        if not self.pl.isVisible:
            pass
        else:
            self.pl.show()

        self.pl.activateWindow()

    def onActionNewFitPage(self):
        self.fitPageCounter += 1
        self.newFitPage = FitPage(self.fitPageCounter)
        self.fittingTabs.addTab(self.newFitPage, "Fit Page " + str(self.fitPageCounter))
        self.fittingTabs.setCurrentIndex(self.fitPageCounter-1)

    def onShowDataViewer(self):
        self.dataviewer.update_datasets_from_collector(self.datacollector)

        if self.dataviewer.isVisible():
            self.dataviewer.hide()
            self.cmdShowDataViewer.setText("Show Data Viewer")
        else:
            self.dataviewer.show()
            self.cmdShowDataViewer.setText("Hide Data Viewer")

    def closeEvent(self, event):
        sys.exit()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
