import time


class Dataset:
    def __init__(self, fitpage_index, x_data, y_data, y_fit, plotpage_index=0):
        self.fitpage_index = fitpage_index
        self.x_data = x_data
        self.y_data = y_data
        self.y_fit = y_fit
        self.plotpage_index = plotpage_index

        self.data_id = self.generate_id(self.fitpage_index)

    def generate_id(self, fitpage_index):
        new_id = float(str(fitpage_index) + str(time.time()))
        print("generated id: ", new_id)
        return new_id

    def get_data_id(self):
        return self.data_id

    def get_fitpage_index(self):
        return self.fitpage_index

    def get_x_data(self):
        return self.x_data

    def get_y_data(self):
        return self.y_data

    def get_y_fit(self):
        return self.y_fit

    def has_y_fit(self):
        if not self.y_fit:
            return False
        else:
            return True

    def get_plotpage_index(self):
        return self.plotpage_index

    def set_plotpage_index(self, plotpage_index):
        if isinstance(plotpage_index, int):
            self.plotpage_index = plotpage_index
        else:
            print("no integer")
