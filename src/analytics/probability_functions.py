import math
import random


def conditional_probability(a_and_b, b):
    """

    Returns the probability: a under the condition of b.

    P(a|b) = P(a ⋂ b) / P(b)


    :param a_and_b:
    :param b:
    :return:

    >>> conditional_probability(0.18, 0.6)
    0.3
    """
    return a_and_b / b


def bayes_theorem(a_and_b, a):
    """
    Returns the probability of b under the condition a.

    P(b|a)  = P(a ⋂ b) / P(a)
            = [P(a|b)*P(b)] / P(a)

    P(a) = P(a ⋂ b) + P(a ⋂ ¬b)


    => P(b|a)  = [P(a|b)*P(b)] / [P(a|b)*P(b) + P(a|¬b)*P(¬b)]

    :return:

    >>> bayes_theorem(0.28, 0.34)
    0.824
    """
    return round(a_and_b / a, 3)


def normal_distribution_probability_density(x, mu=0, sigma=1):
    """
    Often called PDF or Gauss-distribution.
    The area below this function is always equal to 1.
    The area between two points (e.g xa, xb) is equal to the probability that a random value appears between
        those two given points.

    :param x:
    :param mu: Mean or expectation of the distribution
    :param sigma: Standard deviation
    :return:

    >>> normal_distribution_probability_density(0)
    0.3989422804014327
    >>> normal_distribution_probability_density(0, 0, 1)
    0.3989422804014327
    >>> normal_distribution_probability_density(0, 0, 2)
    0.19947114020071635
    >>> normal_distribution_probability_density(0, 0, 0.5)
    0.7978845608028654
    >>> normal_distribution_probability_density(-1, -1, 1)
    0.3989422804014327
    """
    return ((1 / (math.sqrt(2 * math.pi) * sigma))) * math.exp((-1) * (math.pow(x - mu, 2)/(2*math.pow(sigma, 2))))


def cumulative_distribution(x, mu=0, sigma=1):
    """
    Often called CDF. CDF is the integral (so the area) of the PDF.

    Returns the probability that a variable is below the given threshold x.

    CDF is always:
        * not-decreasing
        * lim x --> inf = 1
        * lim x --> -inf = 0


    >>> cumulative_distribution(10000)
    1.0
    >>> cumulative_distribution(-10000)
    0.0
    >>> cumulative_distribution(0)
    0.5
    >>> cumulative_distribution(-2, -2, 0.5)
    0.5

    :param x: Given threshold
    :param mu: Mean or expectation of the distribution
    :param sigma: Standard deviation
    :return:
    """
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2


def inverse_cumulative_distribution(target_probability, mu=0, sigma=1, tolerance=0.00001):
    """
    Returns the x-axis value which would result to a given probability using the CDF.

    :param target_probability:
    :param mu: Mean or expectation of the distribution
    :param sigma: Standard deviation
    :param tolerance
    :return:

    >>> inverse_cumulative_distribution(0.5, 0, 1)
    0.0
    >>> inverse_cumulative_distribution(0.8, 0, 1)
    0.842
    >>> inverse_cumulative_distribution(0.1, 0, 1)
    -1.282
    """
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_cumulative_distribution(target_probability, tolerance=tolerance)

    low_x = -10
    high_x = 10
    mid_x = (low_x + high_x) / 2.0
    p = cumulative_distribution(mid_x, mu, sigma)

    while abs(p - target_probability) > tolerance:
        if p > target_probability:
            high_x = mid_x
        elif p < target_probability:
            low_x = mid_x
        else:
            break
        mid_x = (low_x + high_x) / 2.0
        p = cumulative_distribution(mid_x, mu, sigma)
    return round(mid_x, 3)


def bernoulli_trial(p):
    """

    Returns 1 with the probability of p
    Returns 0 with the probability of (1 - p)

    :param p: Number between 0 and 1
    :return:

    -> This method can't be tested
    """
    return 1 if random.random() < p else 0


def binomial(n, p):
    """
    Returns the sum of n bernoulli-trials with the probability of p

    :param n: Number of bernoulli-trials
    :param p: Probability
    :return:

    -> This method can't be tested
    """
    return sum(bernoulli_trial(p) for _ in range(n))


def normal_approximation_to_binomial(n, p):
    """
    Returns (mu, sigma)
            (expected value, standard deviation)
    :param n: Corresponds to number of bernoulli-trials
    :param p: Probability
    :return:

    >>> normal_approximation_to_binomial(1000, 0.5)
    500.0, 15.811
    """
    mu = n * p
    sigma = math.sqrt(n * p * (1 - p))
    return mu, round(sigma, 3)


def normal_probability_above(low, mu=0, sigma=1):
    """
    Returns the probability that a variable is higher as a given threshold

    :param low: Threshold
    :param mu: Expected value
    :param sigma: Standard deviation
    :return:
    """
    return 1 - cumulative_distribution(low, mu, sigma)


def normal_probability_between(low, high, mu=0, sigma=1):
    """
     Returns the probability that a variable is between two given thresholds.

    :param low: Low-Threshold
    :param high: High-Threshold
    :param mu: Expected value
    :param sigma: Standard deviation

    :return:
    """
    return cumulative_distribution(high, mu, sigma) - cumulative_distribution(low, mu, sigma)


def normal_probability_outside(low, high, mu=0, sigma=1):
    """
     Returns the probability that a variable is outside two given thresholds.

    :param low: Low-Threshold
    :param high: High-Threshold
    :param mu: Expected value
    :param sigma: Standard deviation

    :return:
    """
    return cumulative_distribution(low, mu, sigma) + (1 - cumulative_distribution(high, mu, sigma))


def normal_upper_bound(probability, mu=0, sigma=1):
    """
    Calculates z so that:   P(Z <= z) = probability

    -> Returns a number z so that the chances of a random variable Z being below z
        is equal to the given probability.

    :param probability:
    :param mu:
    :param sigma:
    :return:
    """
    return inverse_cumulative_distribution(probability, mu, sigma)


def normal_lower_bound(probability, mu=0, sigma=1):
    """
    Calculates z so that:   P(Z >= z) = probability

    -> Returns a number z so that the chances of a random variable Z being higher than z
        is equal to the given probability.

    :param probability:
    :param mu:
    :param sigma:
    :return:
        """
    return inverse_cumulative_distribution(1 - probability, mu, sigma)


def normal_two_sided_bounds(probability, mu=0, sigma=1):
    """


                Gauss
                  |
    -------|------+--------|-------
    part_p |  probability  | part_p
           |               |
           v               v
      lower_bound     upper_bound

    :param probability:
    :param mu:
    :param sigma:
    :return:
    """
    # This is the lowest/highest part probability
    part_probability = (1 - probability) / 2.0

    # "part_probability" should be above the higher threshold
    # So "upper_bound" is a threshold where a variable Z will be higher by a chance of "part_probability"
    upper_bound = normal_lower_bound(part_probability, mu, sigma)

    # "part_probability" should be below the lower threshold
    # So "lower_bound" is a threshold where a Variable Z will be smaller by a chance of "part_probability"
    lower_bound = normal_upper_bound(part_probability, mu, sigma)

    return lower_bound, upper_bound


if __name__ == "__main__":
    import doctest
    doctest.testmod()
