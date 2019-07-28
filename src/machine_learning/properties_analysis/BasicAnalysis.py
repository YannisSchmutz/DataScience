import csv
from functools import reduce
from collections import Counter, defaultdict
from matplotlib import pyplot as plt
from pprint import pprint


class BasicAnalysis:

    def __init__(self, data_set):
        self.ds = data_set
        self.ds_length = len(data_set)
        self.prices = list(map(lambda x: x[-1], self.ds))

    def get_mean_price(self):
        return reduce(lambda x, y: x + y, self.prices) / self.ds_length

    def get_highest_price(self):
        return max(self.prices)

    def get_lowest_price(self):
        return min(self.prices)

    def get_median_price(self):
        sorted_prices = sorted(self.prices)
        midpoint = self.ds_length // 2
        if len(self.ds) % 2:
            return sorted_prices[midpoint]
        else:
            hi = sorted_prices[midpoint]
            lo = sorted_prices[midpoint -1]
            return (hi + lo) / 2

    def get_percentile_of_prices(self, p):
        """

        :param p: Float value from 0.0 to 0.99..
        :return:
        """
        sorted_prices = sorted(self.prices)
        p_index = int(p * self.ds_length)
        return sorted_prices[p_index]

    def get_prices_mode(self):
        """
        Returns the prices which appear most often in the data set.
        :return:
        """
        price_counter = Counter(self.prices)
        max_count = max(price_counter.values())
        return [x for x, count in price_counter.items() if count == max_count]

    def show_prices_boxplot(self):
        plt.boxplot(self.prices)
        plt.title("Price box plot")
        plt.show()

    def show_average_zip_code_price(self):

        zip_price_pairs = sorted(list(map(lambda x: (x[2], x[7]), self.ds)), key=lambda x: x[0])

        zip_avg_price_dict = defaultdict(float)
        zips = list(map(lambda x: x[0], zip_price_pairs))

        for zip in zips:
            specific_zip_values = list(map(lambda x: x[1], filter(lambda x: x[0] == zip, zip_price_pairs)))
            specific_zip_len = len(specific_zip_values)
            zip_avg_price_dict[zip] = round(reduce(lambda x,y: x + y, specific_zip_values) / specific_zip_len, 0)

        plt.bar(list(zip_avg_price_dict.keys()), list(zip_avg_price_dict.values()), color="blue")

        plt.xticks(rotation=45)

        plt.title("Average prices per ZIP code")
        plt.ylabel("Price (CHF)")
        plt.xlabel("ZIP codes")
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

    print(data_set)
    print(len(data_set))

    ba = BasicAnalysis(data_set)

    ba.show_prices_boxplot()

    ba.show_average_zip_code_price()
