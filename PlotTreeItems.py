#hier kommen items rein, die dann in dem plottreewidget benutzt werden können
from PyQt6.QtWidgets import QTreeWidgetItem
class TabItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super().__init__(parent, name)

class SubTabItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super().__init__(parent, name)

class PlotItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super().__init__(parent, name)

class PlottableItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super().__init__(parent, name)

