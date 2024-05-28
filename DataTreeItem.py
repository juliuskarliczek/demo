from PyQt6.QtWidgets import QTreeWidgetItem


class DataTreeItem(QTreeWidgetItem):
    def __init__(self, *args, data_id=0):
        super().__init__(*args)
        self.data_id = data_id

