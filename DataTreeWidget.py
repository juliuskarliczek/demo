from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QMimeData, QRect
from PyQt6.QtGui import QDrag


class DataTreeWidget(QTreeWidget):
    def __init__(self, DataViewer):
        super().__init__(parent=DataViewer)
        self.setGeometry(QRect(10, 10, 201, 192))
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.DragOnly)
        self.setColumnCount(1)
        self.setHeaderLabels(["Data Name"])

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()



    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText(item.text(0))
            drag.setMimeData(mimeData)
            drag.exec(supportedActions)
