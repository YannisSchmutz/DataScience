import math
from matplotlib import pyplot as plt
import random
from collections import Counter
from src.analytics.probability_functions import normal_distribution_probability_density as pdf


"""
mu = n*p
sigma = sqrt(n*p*(1-p))


"""


def bernoulli_trial(p):
    """

    Returns 1 with the probability of p
    Returns 0 with the probability of (1 - p)

    :param p:
    :return:
    """
    return 1 if random.random() < p else 0


def binomial(n, p):
    return sum(bernoulli_trial(p) for _ in range(n))


def make_graph(p, n, nbr_of_samples):

    data = [binomial(n, p) for _ in range(nbr_of_samples)]

    # ---- Binomial distribution -------
    # [(value1, how-many-times1), (value2, how-many-times2), ...]
    data_counter = Counter(data)
    print(data_counter.items())

    # Show binomial distribution as bar plot
    plt.bar([x for x in data_counter.keys()],
            [v / nbr_of_samples for v in data_counter.values()],
            label="Binomial distribution")

    # ---- Normal distribution (approximation) ---------
    mu = p * n
    sigma = math.sqrt(n * p * (1 - p))
    # Create range for the x axis
    xs = range(min(data), max(data)+1)
    # Create the corresponding normal distribution
    ys = [pdf(i, mu, sigma) for i in xs]
    plt.plot(xs, ys, color='red', label="Normal Approximation")

    plt.title(f"Binomial Distribution vs. Normal Approximation\np={p}, n={n}, samples={nbr_of_samples},"
              f" mu={mu}, sigma={round(sigma, 3)}")
    plt.legend()
    plt.show()


if __name__ == '__main__':

    make_graph(0.3, 100, 1000)
