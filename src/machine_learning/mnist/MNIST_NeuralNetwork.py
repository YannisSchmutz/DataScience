
import numpy as np
from scipy.special import expit as sigmoid
#%config IPCompleter.greedy=True

from matplotlib import pyplot
#%matplotlib inline

from time import sleep


class NeuralNetwork:
    def __init__(self, nbr_inputnodes, nbr_hiddennodes, nbr_outputnodes, learningrate):
        self.inodes = nbr_inputnodes
        self.hnodes = nbr_hiddennodes
        self.onodes = nbr_outputnodes

        self.learningrate = learningrate

        # self.weight_input_hidden = np.random.uniform(low=-0.99, high=0.99, size=(self.hnodes,self.inodes))
        # self.weight_hidden_output = np.random.uniform(low=-0.99, high=0.99, size=(self.inodes,self.onodes))
        # Use "normal distribution": 1/sqrt(nbr_nodes) = (nbr_nodes)^(-0.5)
        self.weight_input_hidden = np.random.normal(0.0, pow(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.weight_hidden_output = np.random.normal(0.0, pow(self.onodes, -0.5), (self.onodes, self.hnodes))

        self.activation_function = lambda x: sigmoid(x)

    def train(self, inputs_list, targets_list):
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        hidden_inputs = np.dot(self.weight_input_hidden, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        output_errors = targets - final_outputs
        self.weight_hidden_output += self.learningrate * np.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                                                np.transpose(hidden_outputs))

        hidden_errors = np.dot(self.weight_hidden_output.T, output_errors)
        self.weight_input_hidden += self.learningrate * np.dot(
            (hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))

    def query(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T

        # Caculate signals into hidden layer
        # Xhidden = Winput_hidden * I
        hidden_inputs = np.dot(self.weight_input_hidden, inputs)

        # Calculate the signals emerging form hidden layer
        # Ohidden = sigmoid(Xhidden)
        hidden_outputs = self.activation_function(hidden_inputs)

        # Calculate signals into final output layer
        final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)

        # Calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs


def scale_input(input_vector):
    """
    Scales input vector value(s) from 0.01 to 1
    """
    return (input_vector / 255) * 0.99 + 0.01


if __name__ == "__main__":
    input_nodes = 784
    hidden_nodes = 100
    output_nodes = 10

    learning_rate = 0.2
    epoches = 3

    nn = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    # TODO: Do not load whole file in memory...
    with open('mnist_train.csv') as f:
        for e in range(epoches):
            for line in f.readlines():
                line_values = line.split(',')

                targets = np.zeros(output_nodes) + 0.01
                targets[int(line_values[0])] = 0.99

                inputs = scale_input(np.asfarray(line_values[1:]))

                nn.train(inputs, targets)

    with open('mnist_test_10.csv') as f:
        scorecard = []
        for line in f.readlines():
            line_values = line.split(',')
            real_value = int(line_values[0])

            inputs = scale_input(np.asfarray(line_values[1:]))
            outputs = nn.query(inputs)
            ai_prediction = np.argmax(outputs)
            if ai_prediction == real_value:
                scorecard.append(1)
            else:
                scorecard.append(0)
            print(real_value, ai_prediction, outputs)
            pyplot.figure()
            image_array = np.asfarray(line_values[1:]).reshape((28, 28))
            pyplot.imshow(image_array, cmap='Greys', interpolation='None')
        # print(scorecard)
        scorecard_array = np.asarray(scorecard)
        print("Hit ratio: {hit_ratio}".format(hit_ratio=(scorecard_array.sum() / scorecard_array.size)))


