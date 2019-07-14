from matplotlib import pyplot as plt


if __name__ == "__main__":

    movies = ["Star wars", "Monty Python", "Lord of the rings"]
    rankings = [7, 9, 8]

    # This could be used to shift the bars on th x axis
    #shifted_movies = [i - 0.1 for i, _ in enumerate(movies)]

    plt.bar(movies, rankings, color="green")
    #plt.bar(shifted_movies, rankings)

    plt.title("Example bar chart")
    plt.ylabel("Some movie ranking")
    plt.xlabel("Movies")
    plt.show()


