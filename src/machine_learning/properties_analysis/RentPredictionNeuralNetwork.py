from math import e, pow
import csv
from pprint import pprint
from random import shuffle
import numpy as np
from scipy.special import expit as sigmoid


class RentPredictionNeuralNetwork:

    def __init__(self, learning_rate):
        """
        Input matrix
        ............
            i1      # BE
        I = i2      # ZH
            i3      # BS
            i4      # LU
            i5      # rooms
            i6      # area (m^2)

        Weight-Input-Hidden-Matrix
        ..........................
              w11 w21 w31 w41 w51 w61
        Wih = w12 w22 w32 w42 w52 w62
              w13 w23 w33 w43 w53 w63
              w14 w24 w34 w44 w54 w64

        Hidden-Nodes-Matrix
        ...................
            h1
        H = h2
            h3
            h4

        Weight-Hidden-Output-Matrix
        ...........................
        Who = wa wb wc wd

        Output-Matrix
        .............
        O = o1

        H = Whih * I
        O = Who * H

        """
        self._min_room = None
        self._max_room = None
        self._min_area = None
        self._max_area = None
        self._min_price = None
        self._max_price = None

        # Canton use One-Hot-Encoding for the nominal canton values
        self._canton_mapper = {'BE': (1, 0, 0, 0),
                               'ZH': (0, 1, 0, 0),
                               'BS': (0, 0, 1, 0),
                               'LU': (0, 0, 0, 1),
                               }

        self.learning_rate = learning_rate

        # Self-made sigmoid (lambda x: 1/(1 + pow(e, -x))) can't be applied on vectors/ matrices
        self.activation_function = lambda x: sigmoid(x)
        r = lambda: np.random.uniform(low=-0.99, high=0.99)

        self.weight_input_hidden = np.array([[r(), r(), r(), r(), r(), r()],
                                             [r(), r(), r(), r(), r(), r()],
                                             [r(), r(), r(), r(), r(), r()],
                                             [r(), r(), r(), r(), r(), r()],
                                             ])

        self.weight_hidden_output = np.array([r(), r(), r(), r()], ndmin=2)

    def train(self, inputs, target):

        # Transpose has no effect for a 1-D array, therefore set minimum dimension to 2.
        input_nodes = np.array(inputs, ndmin=2).T
        target_node = np.array(target, ndmin=2).T

        hidden_inputs = np.dot(self.weight_input_hidden, input_nodes)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_input = np.dot(self.weight_hidden_output, hidden_outputs)
        final_output = self.activation_function(final_input)

        # TODO: Have a deeper look at this again!
        output_error = target_node - final_output
        self.weight_hidden_output += self.learning_rate * np.dot((output_error * final_output * (1-final_output)),
                                                                 np.transpose(hidden_outputs))

        hidden_error = np.dot(np.transpose(self.weight_hidden_output), output_error)
        self.weight_input_hidden += self.learning_rate * np.dot((hidden_error * hidden_outputs * (1-hidden_outputs)),
                                                                np.transpose(input_nodes))

    def query(self, inputs):
        input_nodes = np.array(inputs, ndmin=2).T

        hidden_inputs = np.dot(self.weight_input_hidden, input_nodes)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_input = np.dot(self.weight_hidden_output, hidden_outputs)
        final_output = self.activation_function(final_input)
        return np.asscalar(final_output)

    def reverse_normalization(self, data):
        reversed_canton_mapper = dict([value, key] for key, value in self._canton_mapper.items())
        reversed_normalization_function = lambda x, _min, _max: round(((x/0.99)-0.01) * (_max - _min) + _min, 1)

        reversed_data = (reversed_canton_mapper[(data[0], data[1], data[2], data[3])],
                         reversed_normalization_function(data[4], self._min_room, self._max_room),
                         reversed_normalization_function(data[5], self._min_area, self._max_area),
                         reversed_normalization_function(data[6], self._min_price, self._max_price)
                         )
        return reversed_data

    def reverse_normalized_price(self, normalized_price):
        price = ((normalized_price/0.99)-0.01) * (self._max_price - self._min_price) + self._min_price
        return round(price, 0)

    def normalize_data_set(self, data_set):

        # Normalizes data in a range from circa 0.01 to 0.99
        #  Avoid 0 as input values because the multiplied wights won't have any impact anymore!
        #  Avoid 1 as output values because 1 can never be reached by sigmoid. -> Weights diverge.
        normalization_function = lambda x, _min, _max: ((x - _min) / (_max - _min) + 0.01) * 0.99

        # Map number of rooms from 0.01 to 0.99
        self._min_room = min(map(lambda rooms: rooms[1], data_set))
        self._max_room = max(map(lambda rooms: rooms[1], data_set))

        self._min_area = min(map(lambda area: area[2], data_set))
        self._max_area = max(map(lambda area: area[2], data_set))

        self._min_price = min(map(lambda price: price[3], data_set))
        self._max_price = max(map(lambda price: price[3], data_set))

        # data_set = list(map(lambda line: (self._canton_mapper[line[0]],
        data_set = list(map(lambda line: (*self._canton_mapper[line[0]],
                                          normalization_function(line[1], self._min_room, self._max_room),
                                          normalization_function(line[2], self._min_area, self._max_area),
                                          normalization_function(line[3], self._min_price, self._max_price),
                                          ), data_set))

        # Shuffle the data set for more variety in small training/ test sets
        shuffle(data_set)
        return data_set


if __name__ == '__main__':

    # Data set1 is 1271 lines long
    # Data set2 is 1051 lines long
    # Total length = 2322
    data_files = ('properties_data_1.csv', 'properties_data_2.csv')

    data_set = []
    for data_file in data_files:
        # Prepare just the data I want to use
        # street,number,plz,place,canton,rooms,area,price
        # -> canton, rooms, area, price
        with open(data_file, 'r') as fh:
            csv_reader = csv.reader(fh, delimiter=',')
            # Skip header
            next(csv_reader)
            data_set.extend(list(map(lambda line: (line[4], float(line[5]), float(line[6]), float(line[7])), csv_reader)))

    # pprint(data_set[:10])
    nn = RentPredictionNeuralNetwork(learning_rate=5)
    # Normalize input values
    data_set = nn.normalize_data_set(data_set)

    train_set = data_set[:2280]
    test_set = data_set[2280:]

    #sample = train_set[0]
    #nn.train(list(sample[:-1]), sample[-1])
    #import sys
    #sys.exit()

    epoches = 11
    for _ in range(epoches):
        for data in train_set:
            # Beware to pass a list and not tuples
            nn.train(list(data[:-1]), data[-1])

    error_sum = 0
    for data in test_set:
        print('-----------------------------------------------------------------------')
        original_data = nn.reverse_normalization(data)
        print(f"Original data: {original_data}")
        res = nn.query(list(data[:-1]))
        reversed_res = nn.reverse_normalized_price(res)
        print(f"NN guess:\t\t\t\t\t\t {reversed_res}")

        error = round((abs(original_data[-1] - reversed_res) / original_data[-1]) * 100, 2)
        print(f"Error: {error} %")
        error_sum += error
        print('-----------------------------------------------------------------------')

    avg_err = round(error_sum / len(test_set), 2)
    print(f"Average error: {avg_err} %")
