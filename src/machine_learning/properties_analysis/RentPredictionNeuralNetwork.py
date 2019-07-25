from math import e, pow
import csv
from pprint import pprint


class RentPredictionNeuralNetwork:

    def __init__(self):
        self.activation_function = lambda x: 1/(1 + pow(e, -x))
        pass

    def train(self):
        pass

    def query(self):
        pass

    @staticmethod
    def normalize_data_set(data_set):

        # Normalizes data in a range from circa 0.01 to 0.99
        #  Avoid 0 as input values because the multiplied wights won't have any impact anymore!
        #  Avoid 1 as output values because 1 can never be reached by sigmoid. -> Weights diverge.
        normalization_function = lambda x, _min, _max: ((x - _min) / (_max - _min) + 0.01) * 0.99

        # Canton value must be a float value from 0.001 to 0.99 and no string
        canton_mapper = {'BE': 0.01,
                         'ZH': 0.5,
                         'BS': 0.99}

        # Map number of rooms from 0.01 to 0.99
        min_room = min(map(lambda rooms: rooms[1], data_set))
        max_room = max(map(lambda rooms: rooms[1], data_set))

        min_area = min(map(lambda area: area[2], data_set))
        max_area = max(map(lambda area: area[2], data_set))

        min_price = min(map(lambda price: price[3], data_set))
        max_price = max(map(lambda price: price[3], data_set))

        data_set = list(map(lambda line: (canton_mapper[line[0]],
                                          normalization_function(line[1], min_room, max_room),
                                          normalization_function(line[2], min_area, max_area),
                                          normalization_function(line[3], min_price, max_price),
                                          ), data_set))

        return data_set


if __name__ == '__main__':

    # Prepare just the data I want to use
    # street,number,plz,place,canton,rooms,area,price
    with open('properties_data_1.csv', 'r') as fh:
        csv_reader = csv.reader(fh, delimiter=',')
        pprint(dir(csv_reader))
        # Skip header
        next(csv_reader)
        data_set = list(map(lambda line: (line[4], float(line[5]), float(line[6]), float(line[7])), csv_reader))

    pprint(data_set[:10])
    # Normalize input values
    data_set = RentPredictionNeuralNetwork.normalize_data_set(data_set)

    train_set = data_set[900:910]
    pprint(train_set)

    nn = RentPredictionNeuralNetwork()


