from matplotlib import pyplot as plt


if __name__ == "__main__":
    caught_fish = ["Pike", "Trout", "Bass", "Barbel"]
    temp = [15, 20, 24, 26]
    depth = [10, 13, 5, 2]
    plt.scatter(temp, depth)

    # Label the points
    for label, x, y in zip(caught_fish, temp, depth):
        plt.annotate(label, (x, y), xytext=(5, -3), textcoords='offset points')
    plt.title("Caught fish")
    plt.xlabel("Temperature in °C")
    plt.ylabel("Water depth")
    plt.show()
