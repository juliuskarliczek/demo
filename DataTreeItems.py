from PyQt6.QtWidgets import QTreeWidgetItem


class PlotPageItem(QTreeWidgetItem):
    def __init__(self, parent, name, data_id):
        super().__init__(parent, name)
        self.data_id = data_id

    def get_data_id(self):
        return self.data_id


class DataItem(QTreeWidgetItem):
    def __init__(self, parent, name, data_id, identifier):
        super().__init__(parent, name)
        self.data_id = data_id
        # self.identifier saves if the item is a data item or a fit item in the tree widget
        # identifier=1 is for data and identifier=2 is for fit
        self.identifier = identifier

    def get_data_id(self):
        return self.data_id

    def get_identifier(self):
        return self.identifier



