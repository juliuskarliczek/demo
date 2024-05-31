from PyQt6.QtWidgets import QTreeWidgetItem


class PlotPageItem(QTreeWidgetItem):
    def __init__(self, parent, name, data_id=0):
        super().__init__(parent, name)
        self.data_id = data_id

    def get_data_id(self):
        return self.data_id
class DataItem(QTreeWidgetItem):
    def __init__(self, parent, name):
        super().__init__(parent, name)

