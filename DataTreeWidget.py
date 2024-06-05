from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QMimeData, QRect, QByteArray, QDataStream, QIODevice
from PyQt6.QtGui import QDrag
from DataTreeItems import DataItem

class DataTreeWidget(QTreeWidget):
    def __init__(self, DataViewer, datacollector):
        super().__init__(parent=DataViewer)
        self.datacollector = datacollector

        self.setGeometry(QRect(10, 10, 291, 212))
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        self.setColumnCount(1)
        self.setHeaderLabels(["Data Name"])

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            if isinstance(item.data(0, 1), DataItem):
                data_id = item.data(0, 1).get_data_id()
                data_type = item.data(0, 1).get_type_num()

                drag = QDrag(self)
                byteArrayID = QByteArray()
                dataStreamID = QDataStream(byteArrayID, QIODevice.OpenModeFlag.WriteOnly)
                dataStreamID.writeDouble(data_id)

                byteArrayType = QByteArray()
                dataStreamType = QDataStream(byteArrayType, QIODevice.OpenModeFlag.WriteOnly)
                dataStreamType.writeInt(data_type)

                mimeData = QMimeData()
                mimeData.setData('DataID', byteArrayID)
                mimeData.setData('TypeNum', byteArrayType)

                fitpage_index = self.datacollector.get_data_id(data_id).get_fitpage_index()
                mimeData.setText("FP " + str(fitpage_index) + " " + self.currentItem().text(0))

                drag.setMimeData(mimeData)
                drag.exec(supportedActions)