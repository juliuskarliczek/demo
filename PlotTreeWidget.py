from PySide6.QtWidgets import QTreeWidget
from PySide6.QtCore import QRect, Signal
from PlotTreeItems import TabItem, SubTabItem, PlotItem, PlottableItem

class PlotTreeWidget(QTreeWidget):
    dropSignal = Signal()
    def __init__(self, DataViewer):
        super().__init__(parent=DataViewer)
        self.setGeometry(QRect(10, 332, 391, 312))
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setColumnCount(1)
        self.setHeaderLabels(["Plot Names"])

    def dragEnterEvent(self, event):
        event.acceptProposedAction()


    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().data('ID'):
            data_id = event.mimeData().data('ID').data()
            data_type = event.mimeData().data('Type').data()
            print(data_id)
            print(data_type)

            targetItem = self.itemAt(event.position().toPoint())
            if isinstance(targetItem.data(0, 1), PlotItem):
                new_plottable = PlottableItem(targetItem, [str(data_id)],
                                              int(data_id), int(data_type))

                self.dropSignal.emit()
                event.acceptProposedAction()
            elif isinstance(targetItem.data(0, 1), PlottableItem):
                # as soon as slots for adjusting are there, the slots can be filled in here
                pass
            else:
                event.ignore()
        else:
            event.ignore()






