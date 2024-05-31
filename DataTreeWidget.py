from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QMimeData, QRect, QByteArray, QDataStream, QIODevice
from PyQt6.QtGui import QDrag


class DataTreeWidget(QTreeWidget):
    def __init__(self, DataViewer, datacollector):
        super().__init__(parent=DataViewer)
        self.datacollector = datacollector

        self.setGeometry(QRect(10, 10, 201, 192))
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        self.setColumnCount(1)
        self.setHeaderLabels(["Data Name"])

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            drag = QDrag(self)
            mimeData = QMimeData()
            if item.parent() is None:
                data_id = self.datacollector.get_data_by_fitpage_index(int(item.text(0).split()[3])).get_data_id()
                mimeData.setText("FP" + "," + str(data_id))
            else:
                data_id = (self.datacollector.
                           get_data_by_fitpage_index(int(item.parent().text(0).split()[3])).get_data_id())
                mimeData.setText(self.currentItem().text(0) + "," + str(data_id))
            drag.setMimeData(mimeData)
            drag.exec(supportedActions)
