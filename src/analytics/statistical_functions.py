from functools import reduce
from collections import Counter

import math
import numpy as np


def mean(data_set):
    """
    Returns the mean value of a given data set.
    :param data_set: List of numbers
    :return:

    >>> mean([1,2,3,4,5])
    3.0
    >>> mean([5,1,2,4,3])
    3.0
    """
    return reduce(lambda x, y: x + y, data_set) / len(data_set)


def median(data_set):
    """
    Returns the median of a given data set.
    :param data_set: List of numbers
    :return:

    Median of an even number of values
    >>> median([10, 7, 5, 1, 3, 6, 4, 8, 9, 2])
    5.5

    Median of an odd number of values
    >>> median([10, 20, 30, 40, 50])
    30
    """
    data_set_length = len(data_set)
    sorted_data_set = sorted(data_set)
    midpoint = data_set_length // 2
    if data_set_length % 2:
        return sorted_data_set[midpoint]
    else:
        hi = sorted_data_set[midpoint]
        lo = sorted_data_set[midpoint - 1]
        return (hi + lo) / 2


def percentile(data_set, p):
    """
    Returns a measure of a given data set indicating a value below a given percentage (p)
    of observations in a group of observations falls.
    :param data_set: List of values
    :param p: Value between 0 and 1
    :return:

    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0)
    1
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.1)
    1
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.2)
    2
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.3)
    3
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.4)
    4
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.5)
    5
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.6)
    6
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.7)
    7
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.8)
    8
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.9)
    9
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1)
    10
    >>> percentile(list(range(0, 1001)), 0.5)
    500
    >>> percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1.1)
    Traceback (most recent call last):
      ...
    ValueError: p must me 0 < p <= 1
    >>> percentile([1, 3, 2, 5, 8, 6, 4, 7, 10, 9], 0.7)
    7
    """
    if p > 1:
        raise ValueError("p must me 0 < p <= 1")
    sorted_data_set = sorted(data_set)
    max_index = len(data_set) - 1

    p_index = int(p * max_index)

    return sorted_data_set[p_index]


def mode(data_set):
    """
    Returns a list of values which appear the most in a given data set.
    :param data_set: List of numbers
    :return:

    >>> mode([1,1,1,1,1,1,2,2,3,3,4,4])
    [1]
    >>> mode([1,2,3,4])
    [1, 2, 3, 4]
    >>> mode([10,17,21,17,33,10])
    [10, 17]
    """
    counter = Counter(data_set)
    max_count = max(counter.values())
    return [x for x, count in counter.items() if count == max_count]


def data_range(data_set):
    """
    Returns the spread between the highest and the lowest value in the given data set.
    :param data_set: List of numbers
    :return:

    >>> data_range([0,3,7,10,5])
    10
    """
    return max(data_set) - min(data_set)


def interquartile_range(data_set):
    """
    Returns the data range but between the
    :param data_set: List of numbers
    :return:

    >>> interquartile_range([1,2,3,4,5,6,7,8])
    4
    """
    return percentile(data_set, 0.75) - percentile(data_set, 0.25)


def mean_deviation(data_set):
    """
    Returns mean deviation
    :param data_set: List of numbers
    :return:

    >>> mean_deviation([1,2,3,4,5])
    [-2.0, -1.0, 0.0, 1.0, 2.0]
    """
    mean_value = mean(data_set)
    return [x - mean_value for x in data_set]


def median_deviation(data_set):
    """
    Returns median deviation
    :param data_set: List of numbers
    :return:

    >>> median_deviation([1,5,7,19,22])
    [-6, -2, 0, 12, 15]
    """
    median_value = median(data_set)
    return [x - median_value for x in data_set]


def variance(data_set):
    """
    Returns the variance of a given data set
    :param data_set: List of numbers
    :return:

    >>> variance([1,2,3,4,5,6,7,8,9,10])
    9.167
    >>> variance([1,1,1,2,2,2,2,3,3,3])
    0.667
    >>> variance([1,10,100])
    2997.0
    """
    deviations = mean_deviation(data_set)
    return round(sum(map(lambda x: x * x, deviations)) / (len(data_set) - 1), 3)


def standard_deviation(data_set):
    """

    :param data_set:
    :return:
    >>> standard_deviation([1,2,3,4,5])
    1.581
    """
    return round(math.sqrt(variance(data_set)), 3)


def covariance(data_set1, data_set2):
    """
    Returns the covariance of two data sets.

    High value:         The data sets are some kind proportionally related (+/-)
    Value near null:    The data sets do not depend on each other.

    :param data_set1:
    :param data_set2:
    :return:
    >>> covariance([1,2,3,4,5], [3,4,5,6,7])
    2.5
    """
    n = len(data_set1)
    return np.dot(mean_deviation(data_set1), mean_deviation(data_set2)) / (n - 1)


def correlation(data_set1, data_set2):
    """
    Returns a value between -1 and 1.
    Where a value near +/- 1 indicates a high correlation, a value near zero indicates a low correlation.

    :param data_set1:
    :param data_set2:
    :return:
    """
    stdev1 = standard_deviation(data_set1)
    stdev2 = standard_deviation(data_set2)

    if stdev1 > 0 and stdev2 > 0:
        return round(covariance(data_set1, data_set2) / stdev1 / stdev2, 3)
    else:
        return 0


def get_linear_regression_parameters(x_values, y_values):
    """
    >>> get_linear_regression_parameters([1,2,3,4,5,6,7,8,9,10],[1,2,3,4,5,6,7,8,9,10])
    (1.0, 0.0)

    >>> get_linear_regression_parameters(range(0,10), list(map(lambda x: x*2, range(0,10))))
    (2.0, 0.0)

    >>> get_linear_regression_parameters(range(0,10), list(map(lambda x: x*2 + 3, range(0,10))))
    (2.0, 3.0)

    >>> get_linear_regression_parameters(range(0,10), list(map(lambda x: x*2 - 1, range(0,10))))
    (2.0, -1.0)

    :param x_values: List of numbers
    :param y_values: List of numbners
    :return:
    """
    mean_x = mean(x_values)
    mean_y = mean(y_values)
    numerator = sum(map(lambda i: i[0] * i[1], list(zip([x - mean_x for x in x_values],
                                                        [y - mean_y for y in y_values]))))
    denominator = sum(map(lambda x: x * x, [x - mean_x for x in x_values]))
    m = numerator / denominator
    q = mean_y - m * mean_x
    return m, q


def get_linear_regression_function(x_values, y_values):
    """

    :param x_values:
    :param y_values:
    :return:
    """
    m, q = get_linear_regression_parameters(x_values, y_values)
    f = lambda x: m*x + q
    return f


if __name__ == "__main__":
    import doctest
    doctest.testmod()
