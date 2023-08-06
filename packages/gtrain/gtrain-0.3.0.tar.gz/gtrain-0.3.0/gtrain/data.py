import math

from abc import ABC


class Data(ABC):
    """
    Abstraction of the data for gtrain learning process
    """
    def set_placeholders(self, pl_list):
        """
        set placeholders obtained from the model
        :param pl_list: a list of laceholders
        """
        self.placeholders = pl_list

    def get_next_batch(self):
        """
        :return: next batch of the data as a dictionary that feeds method Session.run
        """
        pass

    def accumulate_grad(self):
        """
        If the True is returned then the learning procedure accumulates gradient and other measures
        :return: a bool value
        """
        pass

    def accumulate_dev(self):
        """
        If the True is returned then the learning procedure accumulates gradient and other measures
        :return: a bool value
        """
        return self.accumulate_grad()

    def get_next_dev_batch(self):
        """
        :return: next batch of the data as a dictionary that feeds method Session.run
        """
        pass

    def train_ended(self):
        """
        function that is called after the training ends.
        """
        pass


class AllData(Data):
    """
    Example of a subclass of the Data class
    - make simple learning procedure where the gradient is computed from all data samples each time
    """

    def __init__(self, train_input, train_target, test_input, test_target):
        self.train_input = train_input
        self.train_target = train_target
        self.test_input = test_input
        self.test_target = test_target
        self.counter = False

    def set_placeholders(self, pl_list):
        self.ph_x = pl_list[0]
        self.ph_y = pl_list[1]

    def get_next_batch(self):
        return {self.ph_x: self.train_input, self.ph_y: self.train_target}

    def accumulate_grad(self):
        return False

    def accumulate_dev(self):
        return False

    def get_next_dev_batch(self):
        return {self.ph_x: self.test_input, self.ph_y: self.test_target}

    def train_ended(self):
        pass


class BatchedData(Data):
    """
    Example of a subclass of the Data class
    - make learning procedure where the gradient is computed from subset of the data so-called batches
    """

    def __init__(self, train_input, train_target, test_input, test_target, batch_size=32):
        self.train_input = train_input
        self.train_target = train_target
        self.test_input = test_input
        self.test_target = test_target
        self.batch_size = batch_size
        self.batch_num = math.ceil(train_input.shape[0] / batch_size)
        self.counter = 0
        self.start_index = 0
        self.end_index = batch_size - 1

    def set_placeholders(self, pl_list):
        self.ph_x = pl_list[0]
        self.ph_y = pl_list[1]

    def get_next_batch(self):
        feet_dict = {
            self.ph_x: self.train_input[self.start_index:self.end_index],
            self.ph_y: self.train_target[self.start_index:self.end_index]}
        if self.end_index == self.train_input.shape[0] - 1:
            self.start_index = 0
            self.end_index = self.batch_size - 1
        else:
            if self.end_index + self.batch_size >= self.train_input.shape[0]:
                self.end_index = self.train_input.shape[0] - 1
            else:
                self.end_index += self.batch_size
            self.start_index += self.batch_size
        return feet_dict

    def accumulate_grad(self):
        return False
        self.counter += 1
        if self.counter % self.batch_num == 0:
            self.counter = 0
            return False
        else:
            return True

    def accumulate_dev(self):
        return False

    def get_next_dev_batch(self):
        return {self.ph_x: self.test_input, self.ph_y: self.test_target}

    def train_ended(self):
        pass
