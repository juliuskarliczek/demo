from PyQt6.QtWidgets import QTreeWidgetItem


class PlotPageItem(QTreeWidgetItem):
    def __init__(self, parent, name, fitpage_index, data_id):
        super().__init__(parent, name)
        self.fitpage_index = fitpage_index
        self.data_id = data_id

    def get_data_id(self):
        return self.data_id


class DataItem(PlotPageItem):
    def __init__(self, parent, name, fitpage_index, data_id, type_num):
        super().__init__(parent, name, fitpage_index, data_id)
        # self.type_num saves if the item is a data item or a fit item in the tree widget
        # identifier=1 is for data and identifier=2 is for fit
        self.type_num = type_num

    def get_type_num(self):
        return self.type_num



