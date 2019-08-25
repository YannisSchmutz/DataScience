from src.analytics.probability_functions import normal_distribution_probability_density as pdf
from src.analytics.probability_functions import cumulative_distribution as cdf
from src.analytics.statistical_functions import mean, standard_deviation
from matplotlib import pyplot as plt


fig, ((sub1, sub2), (sub3, sub4)) = plt.subplots(2, 2)

xs = [x / 10.0 for x in range(-50, 50)]

sub1.plot(xs, [pdf(x) for x in xs], '-', label="mu=0, sigma=1")
sub1.plot(xs, [pdf(x, 0, 2) for x in xs], '.', label="mu=0, sigma=1")
sub1.plot(xs, [pdf(x, 0, 0.5) for x in xs], ':', label="mu=0, sigma=0.5")
sub1.plot(xs, [pdf(x, -1, 1) for x in xs], '-.', label="mu=-1, sigma=1")
sub1.legend()
sub1.set_title("Some normal distribution probability density functions")

sub3.plot(xs, [cdf(x) for x in xs], '-', label="mu=0, sigma=1")
sub3.plot(xs, [cdf(x, 0, 2) for x in xs], '.', label="mu=0, sigma=1")
sub3.plot(xs, [cdf(x, 0, 0.5) for x in xs], ':', label="mu=0, sigma=0.5")
sub3.plot(xs, [cdf(x, -1, 1) for x in xs], '-.', label="mu=-1, sigma=1")
sub3.legend()
sub3.set_title("Some normal cumulative distribution functions")

xs2 = [x / 10.0 for x in range(-30, 20)]
m = mean(xs2)
sd = standard_deviation(xs2)

sub2.plot(xs2, [pdf(x, m, sd) for x in xs2], label=f"mu={m}\n"
                                                   f"sigma={sd}\n"
                                                   f"deviation={sd}")
sub2.legend()
sub2.set_title("ND with calculated mu & sigma")

sub4.plot(xs2, [cdf(x, m, sd) for x in xs2], label=f"mu={m}\n"
                                                   f"sigma={sd}\n"
                                                   f"deviation={sd}")

sub4.legend()
sub4.set_title("Integral of the above ND function")

plt.show()
