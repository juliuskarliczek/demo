from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import QMimeData, QRect, QDataStream, QIODevice
from PyQt6.QtGui import QDrag
from PlotTreeItems import TabItem, SubTabItem, PlotItem, PlottableItem

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
        if not event.mimeData().data('DataID').isEmpty():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if isinstance(self.itemAt(event.position().toPoint()), QTreeWidgetItem):
            if self.itemAt(event.position().toPoint()).data(0, 1) is not None:
                if isinstance(self.itemAt(event.position().toPoint()).data(0, 1), PlotItem):
                    event.acceptProposedAction()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not event.mimeData().data('DataID').isEmpty():
            qds_id = QDataStream(event.mimeData().data('DataID'), QIODevice.OpenModeFlag.ReadOnly)
            qds_type = QDataStream(event.mimeData().data('DataType'), QIODevice.OpenModeFlag.ReadOnly)
            targetItem = self.itemAt(event.position().toPoint())

            if isinstance(targetItem.data(0, 1), PlotItem):
                new_plottable = PlottableItem(targetItem, [event.mimeData().text()],
                                              qds_id.readDouble(), qds_type.readInt())
                print("accepted id: ", qds_id.readDouble())
                print("accepted type: ", qds_type.readInt())
                new_plottable.setData(0, 1, new_plottable)
            elif isinstance(targetItem.data(0, 1), PlottableItem):
                # as soon as slots for adjusting are there, here the slots can be filled
                pass
            event.acceptProposedAction()
        else:
            event.ignore()





