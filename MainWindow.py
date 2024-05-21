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

    def closeEvent(self, event):
        sys.exit()

    def send_data_to_subtab(self, fitpage_from, fitpage_to, subtab_index):
        if self.pl is not None:
            self.pl.send_data_to_subtab(fitpage_from, fitpage_to, subtab_index)
        else:
            pass


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
