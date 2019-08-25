from matplotlib import pyplot as plt


if __name__ == "__main__":
    years = list(range(1950, 2020, 10))
    print(years)
    base_volume = 1000000
    mul = 1.3
    volume = []
    for i in range(len(years)):
        if len(volume) < 1:
            volume.append(base_volume)
        else:
            volume.append(round(volume[i-1] * mul))
    print(volume)

    plt.plot(years, volume, 'g:', label="Volume over years")
    plt.title("Example line chart")
    plt.ylabel("Volume $")
    plt.xlabel("Years")
    plt.legend(loc=9)
    plt.show()


