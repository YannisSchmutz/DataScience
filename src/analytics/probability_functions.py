import math


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
    Often called CDF. CDF is the integral of the PDF.
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

    :param x:
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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
