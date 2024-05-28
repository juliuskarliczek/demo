#class to keep track of all datasets of fitpages and more
import RandomDatasetCreator
from Dataset import Dataset


class DataCollector:
    def __init__(self):
        self.datasets = []
        self.datasetcreator = RandomDatasetCreator.DatasetCreator()

    def update_dataset(self, main_window, fitpage_index, create_fit):
        existing_dataset_index = -1
        for i in range(len(self.datasets)):
            if self.datasets[i].get_fitpage_index() == fitpage_index:
                existing_dataset_index = i

        if existing_dataset_index == -1:
            self.create_dataset(main_window, fitpage_index, create_fit)
        else:
            dataset = self.create_simulated_data(main_window, fitpage_index, create_fit)
            plot_index = self.datasets[existing_dataset_index].get_plotpage_index()
            self.datasets[existing_dataset_index] = Dataset(fitpage_index, dataset.get_x_data(), dataset.get_y_data(), dataset.get_y_fit(), plot_index)

    def create_dataset(self, main_window, fitpage_index, create_fit):
        dataset = self.create_simulated_data(main_window, fitpage_index, create_fit)
        plotpage_index = -1

        dataset = Dataset(fitpage_index, dataset.get_x_data(), dataset.get_y_data(), dataset.get_y_fit(), plotpage_index)
        self.datasets.append(dataset)

    def create_simulated_data(self, main_window, fitpage_index, create_fit):
        combobox_index = main_window.fittingTabs.currentWidget().get_combobox_index()
        int_identifier_parameter = main_window.fittingTabs.currentWidget().get_int_identifier()
        param_scale = main_window.fittingTabs.currentWidget().doubleSpinBox_scale.value()
        param_radius = main_window.fittingTabs.currentWidget().doubleSpinBox_radius.value()
        param_height = main_window.fittingTabs.currentWidget().doubleSpinBox_height.value()

        x_dataset, y_dataset, y_fit = self.datasetcreator.createRandomDataset(param_scale, param_radius, param_height,
                                                                              combobox_index, create_fit)
        dataset = Dataset(fitpage_index, x_dataset, y_dataset, y_fit)

        return dataset

    def get_datasets(self):
        return self.datasets

    def get_data_by_fitpage_index(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i].get_fitpage_index():
                return self.datasets[i]

    def get_x_data(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i].get_fitpage_index():
                return self.datasets[i].get_x_data()

    def get_y_data(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i].get_fitpage_index():
                return self.datasets[i].get_y_data()

    def get_y_fit_data(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i].get_fitpage_index():
                return self.datasets[i].get_y_fit()

    def get_plotpage_index(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i].get_fitpage_index():
                return self.datasets[i].get_plotpage_index()

    def set_plot_index(self, fitpage_index, plot_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i].get_fitpage_index():
                self.datasets[i].set_plotpage_index(plot_index)

