from src.analytics.probability_functions import normal_approximation_to_binomial
from src.analytics.probability_functions import cumulative_distribution as normal_probability_below
from src.analytics.probability_functions import normal_two_sided_bounds
from src.analytics.probability_functions import normal_upper_bound
from src.analytics.probability_functions import normal_probability_between


if __name__ == '__main__':
    # mu, sigma for the hypothesis H0 that a coin flip has a change of 50:50 to land on head
    mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
    print(mu_0, sigma_0)

    # Boundaries for a 95%-threshold based on the assumption that the chances are 50:50 (p = 0.5)
    low_0, high_0 = normal_two_sided_bounds(0.95, mu_0, sigma_0)
    print(low_0, high_0)

    # mu, sigma for the hypothesis that a coin DOES NOT has a change of 50:50 (e.g: p = 0.55)
    mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
    print(mu_1, sigma_1)

    # There is just a 11.3% chance to be in the range of [469;531] if p was 0.55
    type_2_probability = normal_probability_between(low_0, high_0, mu_1, sigma_1)
    print(type_2_probability)
    # Therefore a 88.7% chance to land outside the range of [469;531]
    power = 1 - type_2_probability  # ==> normal_probability_outside(low_0, high_0, mu_1, sigma_1)
    print(power)

    # hi = number for which 95% of all random variables are below
    hi = normal_upper_bound(0.95, mu_0, sigma_0)
    print(hi)  # 526

    # Probability, for the assumption that p was 0.55, that a random variable would be
    #   below 526
    type_2_probability_ = normal_probability_below(hi, mu_1, sigma_1)
    print(type_2_probability_)  # circa 6%
    power_ = 1 - type_2_probability_
    print(power_)
