

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
