#class to keep track of all datasets of fitpages and more
import RandomDatasetCreator


class DataCollector:
    def __init__(self):
        self.datasets = []
        self.datasetcreator = RandomDatasetCreator.DatasetCreator()

    def update_dataset(self, main_window, fitpage_index):
        existing_dataset_index = -1
        for i in range(len(self.datasets)):
            if self.datasets[i][0] == fitpage_index:
                existing_dataset_index = i

        if existing_dataset_index == -1:
            self.create_dataset(main_window, fitpage_index)
        else:
            new_dataset = self.create_simulated_data(main_window, fitpage_index)
            plot_index = self.datasets[existing_dataset_index][5]
            self.datasets[existing_dataset_index] = [fitpage_index, new_dataset[1], new_dataset[2], new_dataset[3],
                                                     new_dataset[4], plot_index]

    def create_dataset(self, main_window, fitpage_index):
        data = self.create_simulated_data(main_window, fitpage_index)
        plotpage_index = -1

        dataset = [fitpage_index, data[1], data[2], data[3], data[4], plotpage_index]
        self.datasets.append(dataset)

    def create_simulated_data(self, main_window, fitpage_index):
        show_graphs = (main_window.cbData.isChecked(),
                       main_window.cbFit.isChecked(),
                       main_window.cbResiduals.isChecked())
        combobox_index = main_window.fittingTabs.currentWidget().get_combobox_index()
        int_identifier_parameter = main_window.fittingTabs.currentWidget().get_int_identifier()
        param_scale = main_window.fittingTabs.currentWidget().doubleSpinBox_scale.value()
        param_radius = main_window.fittingTabs.currentWidget().doubleSpinBox_radius.value()
        param_height = main_window.fittingTabs.currentWidget().doubleSpinBox_height.value()

        x_dataset, y_dataset, y_fit = self.datasetcreator.createRandomDataset(param_scale, param_radius, param_height,
                                                                              combobox_index)
        dataset = [fitpage_index, x_dataset, y_dataset, y_fit, show_graphs]

        return dataset
    def get_data_by_fitpage_index(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i][0]:
                return self.datasets[i]

    def get_show_graphs(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i][0]:
                return self.datasets[i][4]


    #um zu plotten sollte der datacollector übergeben werden und der index, der im datacollector zu dem richtigen dataset zeigt

    #allgemein: was muss beachtet werden, wenn es mehrere fitpages gibt und manche replottet werden sollen,
    #weil sich ihre daten geändert haben? wer ist für das feature zuständig und hält die daten?

    #welche schnittstelle entscheidet, wann geplottet wird?
    #refactoring vom bereits existierenden teil des programms, weil zu kompliziert?
    #data explorer - hat die daten und kommuniziert nicht direkt mit der plot funktion?
    #plot explorer - alle plots werden gelistet und

    #serialize the data and make them a collection with the fitting page index?

    def get_x_data(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i][0]:
                return self.datasets[i][1]

    def get_y_data(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i][0]:
                return self.datasets[i][2]

    def get_y_fit_data(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i][0]:
                return self.datasets[i][3]

    def get_plot_index(self, fitpage_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i][0]:
                return self.datasets[i][5]

    def set_plot_index(self, fitpage_index, plot_index):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i][0]:
                self.datasets[i][5] = plot_index

    def set_show_graphs(self, fitpage_index, show_graphs):
        for i in range(len(self.datasets)):
            if fitpage_index == self.datasets[i][0]:
                self.datasets[i][4] = show_graphs

    def get_datasets(self):
        return self.datasets
