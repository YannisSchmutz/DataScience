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
            i1
        I = i2
            i3

        Weight-Input-Hidden-Matrix
        ..........................
        Wih = w11 w21 w31
              w12 w22 w32

        Hidden-Nodes-Matrix
        ...................
        H = h1
            h2

        Weight-Hidden-Output-Matrix
        ...........................
        Who = w4 w5

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
        # Canton value must be a float value from 0.001 to 0.99 and no string
        self._canton_mapper = {'BE': 0.01,
                               'ZH': 0.5,
                               'BS': 0.99}

        self.learning_rate = learning_rate

        # Self-made sigmoid (lambda x: 1/(1 + pow(e, -x))) can't be applied on vectors/ matrices
        self.activation_function = lambda x: sigmoid(x)
        r = lambda: np.random.uniform(low=-0.99, high=0.99)

        self.weight_input_hidden = np.array([[r(), r(), r()],
                                             [r(), r(), r()]])
        self.weight_hidden_output = np.array([r(), r()], ndmin=2)

        #print(self.weight_input_hidden)
        #print(self.weight_hidden_output)

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

    def reverse_normalisation(self, data):
        reversed_canton_mapper = dict([value, key] for key, value in self._canton_mapper.items())
        reversed_normalization_function = lambda x, _min, _max: round(((x/0.99)-0.01) * (_max - _min) + _min, 1)

        reversed_data = (reversed_canton_mapper[data[0]],
                         reversed_normalization_function(data[1], self._min_room, self._max_room),
                         reversed_normalization_function(data[2], self._min_area, self._max_area),
                         reversed_normalization_function(data[3], self._min_price, self._max_price)
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

        data_set = list(map(lambda line: (self._canton_mapper[line[0]],
                                          normalization_function(line[1], self._min_room, self._max_room),
                                          normalization_function(line[2], self._min_area, self._max_area),
                                          normalization_function(line[3], self._min_price, self._max_price),
                                          ), data_set))

        # Shuffle the data set for more variety in small training/ test sets
        shuffle(data_set)
        return data_set


if __name__ == '__main__':

    # Prepare just the data I want to use
    # street,number,plz,place,canton,rooms,area,price
    # -> canton, rooms, area, price
    # Data set is 1271 lines long
    with open('properties_data_1.csv', 'r') as fh:
        csv_reader = csv.reader(fh, delimiter=',')
        # Skip header
        next(csv_reader)
        data_set = list(map(lambda line: (line[4], float(line[5]), float(line[6]), float(line[7])), csv_reader))

    # pprint(data_set[:10])
    nn = RentPredictionNeuralNetwork(learning_rate=3)
    # Normalize input values
    data_set = nn.normalize_data_set(data_set)

    train_set = data_set[:1260]
    test_set = data_set[1260:1271]
    # pprint(train_set)


    #sample = train_set[0]
    #nn.train(list(sample[:-1]), sample[-1])

    epoches = 3
    for _ in range(epoches):
        for data in train_set:
            # Beware to pass a list and not tuples
            nn.train(list(data[:-1]), data[-1])

    error_sum = 0
    for data in test_set:
        print('-----------------------------------------------------------------------')
        original_data = nn.reverse_normalisation(data)
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


