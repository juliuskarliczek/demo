import sys
from PyQt6 import QtWidgets

from MainWindowUI import Ui_MainWindow
from PlotWidget import PlotWidget
from FitPage import FitPage

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Tabbed Plot Demo")

        self.setMinimumSize(700, 700)

        self.cmdCreatePlot.clicked.connect(self.onCreatePlot)
        self.actionNewFitPage.triggered.connect(self.onActionNewFitPage)
        self.fitPageCounter = 1
        self.newFitPage = FitPage(int_identifier=self.fitPageCounter)
        self.fittingTabs.addTab(self.newFitPage, "Fit Page "+str(self.fitPageCounter))
        self.labelWarning.hide()

        self.pl = None

    def onCreatePlot(self):
        show_graphs = (self.cbData.isChecked(), self.cbFit.isChecked(), self.cbResiduals.isChecked())

        if not (show_graphs[0] or show_graphs[1] or show_graphs[2]):
            self.labelWarning.show()
            return
        self.labelWarning.hide()

        combobox_index = self.fittingTabs.currentWidget().get_combobox_index()
        int_identifier_parameter = self.fittingTabs.currentWidget().get_int_identifier()
        param_scale = self.fittingTabs.currentWidget().doubleSpinBox_scale.value()
        param_radius = self.fittingTabs.currentWidget().doubleSpinBox_radius.value()
        param_height = self.fittingTabs.currentWidget().doubleSpinBox_height.value()

        if self.pl is None:
            self.pl = PlotWidget(param_scale, param_radius, param_height, show_graphs, int_identifier_parameter, combobox_index)
        else:
            self.pl.createNewTab(param_scale, param_radius, param_height, show_graphs, int_identifier_parameter, combobox_index)

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


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
