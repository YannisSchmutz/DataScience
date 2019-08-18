import csv
from functools import reduce
from collections import Counter, defaultdict
from matplotlib import pyplot as plt
from pprint import pprint
from src.analytics.statistical_functions import variance, correlation


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
            avg_price_dict[feature] = round(reduce(lambda x, y: x + y, specific_feature_values) / specific_feature_len, 0)

        plt.bar(list(avg_price_dict.keys()), list(avg_price_dict.values()), color=color)
        plt.xticks(rotation=rotation)

        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.show()

    def get_price_variance(self):
        return variance(self.prices)

    def get_feature_price_correlation(self, feature):
        return correlation(list(map(lambda x: x[self._index_map[feature]], self.ds)), self.prices)

    def show_scatter_plot(self, feature):
        sorted_ds = sorted(self.ds, key=lambda x: x[self._index_map[feature]])
        features = list(map(lambda x: x[self._index_map[feature]], sorted_ds))
        prices = list(map(lambda x: x[self._index_map["price"]], sorted_ds))

        plt.scatter(features, prices)
        plt.title(f"Scatter-plot showing the relation between {feature} and price")
        plt.ylabel("Price CHF")
        plt.xlabel(feature)
        plt.show()


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

    ba.show_average_price_per_feature("area", "Average price per square meters", "Square meters", "Average price CHF")
    ba.show_average_price_per_feature("rooms", "Average price per number of rooms", "Number of rooms", "Average price CHF")

    print(ba.get_feature_price_correlation("area"))
    ba.show_scatter_plot("area")
    print(ba.get_feature_price_correlation("rooms"))
    ba.show_scatter_plot("rooms")
