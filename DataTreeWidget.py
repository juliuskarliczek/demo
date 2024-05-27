from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QMimeData, QRect
from PyQt6.QtGui import QDrag


class DataTreeWidget(QTreeWidget):
    def __init__(self, DataViewer):
        super().__init__(parent=DataViewer)
        self.setGeometry(QRect(10, 10, 201, 192))
        self.setDragEnabled(True)
        self.setColumnCount(1)
        self.setHeaderLabels(["Data Name"])

        #self.currentItemChanged.connect(self.onCurrentItemChanged)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText(item.text(0))
            drag.setMimeData(mimeData)
            drag.exec(supportedActions)

    def onCurrentItemChanged(self, current, previous):
        if current:
            print(f"Current item changed to {current.text(0)}")
        if previous:
            print(f"Previous item was: {previous.text(0)}")
