# Form implementation generated from reading ui file 'DataViewerUI.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DataViewer(object):
    def setupUi(self, DataViewer):
        DataViewer.setObjectName("DataViewer")
        DataViewer.resize(400, 300)
        self.datasetList = QtWidgets.QListWidget(parent=DataViewer)
        self.datasetList.setGeometry(QtCore.QRect(10, 10, 256, 192))
        self.datasetList.setObjectName("datasetList")
        self.cmdSendToPlotpage = QtWidgets.QPushButton(parent=DataViewer)
        self.cmdSendToPlotpage.setGeometry(QtCore.QRect(280, 10, 101, 24))
        self.cmdSendToPlotpage.setObjectName("cmdSendToPlotpage")

        self.retranslateUi(DataViewer)
        QtCore.QMetaObject.connectSlotsByName(DataViewer)

    def retranslateUi(self, DataViewer):
        _translate = QtCore.QCoreApplication.translate
        DataViewer.setWindowTitle(_translate("DataViewer", "Form"))
        self.cmdSendToPlotpage.setText(_translate("DataViewer", "Send to Plotpage"))
