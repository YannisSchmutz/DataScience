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
    :param mu: Mean or expectation of the distribution (
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

    :return:
    """
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2


if __name__ == "__main__":
    import doctest
    doctest.testmod()
