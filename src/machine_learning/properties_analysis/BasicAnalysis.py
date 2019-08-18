import csv
from functools import reduce
from collections import Counter, defaultdict
from matplotlib import pyplot as plt
from pprint import pprint
from src.analytics.base_math_functions import mean, mean_deviation


class BasicAnalysis:

    def __init__(self, data_set):
        self.ds = data_set
        self.ds_length = len(data_set)
        self.prices = list(map(lambda x: x[-1], self.ds))

        # street,number,plz,place,canton,rooms,area,price
        self._index_map = {'street': 0,
                           'number': 1,
                           'plz': 2,
                           'place': 3,
                           'canton': 4,
                           'rooms': 5,
                           'area': 6,
                           'price': 7,
                           }

    def show_prices_boxplot(self):
        plt.boxplot(self.prices)
        plt.title("Price box plot")
        plt.show()

    def show_average_price_per_feature(self, feature, title, xlabel, ylabel, color="blue", rotation=45):
        if feature not in self._index_map.keys():
            raise ValueError("Selected feature is not available! Use one of the following {feats}".format(
                feats=self._index_map.keys()
            ))

        feature_index = self._index_map[feature]
        price_index = self._index_map["price"]
        feature_price_pairs = sorted(list(map(lambda x: (x[feature_index], x[price_index]), self.ds)),
                                     key=lambda x: x[0])

        avg_price_dict = defaultdict(float)
        features = list(map(lambda x: x[0], feature_price_pairs))

        for feature in features:
            specific_feature_values = list(map(lambda x: x[1], filter(lambda x: x[0] == feature, feature_price_pairs)))
            specific_feature_len = len(specific_feature_values)
            avg_price_dict[feature] = round(reduce(lambda x,y: x + y, specific_feature_values) / specific_feature_len, 0)

        plt.bar(list(avg_price_dict.keys()), list(avg_price_dict.values()), color=color)
        plt.xticks(rotation=rotation)

        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()

    def get_price_deviations(self):
        mean_price = mean(self.prices)
        return [xi - mean_price for xi in self.prices]

    def get_price_variance(self):
        if len(self.prices) < 2:
            raise ValueError("Length of prices must be at least 2")
        price_deviations = mean_deviation(self.prices)
        return sum(map(lambda x: x * x, price_deviations)) / (self.ds_length - 1)


if __name__ == '__main__':

    with open('properties_data_1.csv', 'r') as fh:
        csv_reader = csv.reader(fh, delimiter=',')
        # Skip header
        next(csv_reader)
        data_set = list(map(lambda line: (*line[:5], float(line[5]), float(line[6]), float(line[7])),
                            #filter(lambda x: x[3] == 'Bern', csv_reader)))
                            csv_reader
                            ))

    print(data_set[0])

    ba = BasicAnalysis(data_set)

    ba.show_average_price_per_feature("area", "Average price per sqare meters", "Square meters", "Average price CHF")
