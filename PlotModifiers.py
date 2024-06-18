from PySide6.QtWidgets import QTreeWidgetItem

class PlotModifier(QTreeWidgetItem):
    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.setData(0, 1, self)

class ModifierLinestyle(PlotModifier):
    def __init__(self, parent, name):
        super().__init__(parent, name)


class ModifierLinecolor(PlotModifier):
    def __init__(self, parent, name):
        super().__init__(parent, name)


class ModifierColormap(PlotModifier):
    def __init__(self, parent, name):
        super().__init__(parent, name)