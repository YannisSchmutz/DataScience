import math
from matplotlib import pyplot as plt
from collections import Counter
from src.analytics.probability_functions import normal_distribution_probability_density as pdf
from src.analytics.probability_functions import binomial


def make_graph(p, n, nbr_of_samples):
    """
    This creates a graph displaying the binomial distribution as well as an approximation of the normal distribution.

    :param p: Probability
    :param n: Number of bernoulli-trials for each sample value
    :param nbr_of_samples: Number of samples
    :return:
    """

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
