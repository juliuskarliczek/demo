from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QMimeData, QRect, QDataStream
from PyQt6.QtGui import QDrag

class PlotTreeWidget(QTreeWidget):
    def __init__(self, DataViewer):
        super().__init__(parent=DataViewer)
        self.setGeometry(QRect(10, 252, 201, 192))
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.DropOnly)
        self.setColumnCount(1)
        self.setHeaderLabels(["Plot Names"])

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            dataText = event.mimeData().text().split(",")[0]
            print("plottreewidget mimeData text split [0]", dataText)
            print("plottreewidget mimeData text", event.mimeData().text())
            if dataText == "Data" or dataText == "Fit":
                targetItem = self.itemAt(event.position().toPoint())
                newItem = QTreeWidgetItem()
                newItem.setText(0, event.mimeData().text())
                if targetItem:
                    targetItem.addChild(newItem)
                else:
                    self.addTopLevelItem(newItem)

                event.acceptProposedAction()



