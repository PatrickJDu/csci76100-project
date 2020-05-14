#Neural network for feedforward propagation
import numpy as np
import Config

#Neural net weights from Config
num_w0 = Config.num_w0
num_w1 = Config.num_w1
num_w2 = Config.num_w2
num_w3 = Config.num_w3

#Shapes of neural net matrices
W1_shape = (num_w1, num_w0)
W2_shape = (num_w2, num_w1)
W3_shape = (num_w3, num_w2)

#Function to populate neural net matrices from input weights
def splice_weights(weights):
    W1 = weights[0: num_w1*num_w0]
    W2 = weights[num_w1*num_w0 : num_w2*num_w1 + num_w1*num_w0]
    W3 = weights[num_w2*num_w1 + num_w1*num_w0 :]

    return (W1.reshape(num_w1, num_w0), W2.reshape(num_w2, num_w1), W3.reshape(num_w3, num_w2))

#Sigmoid activation function
def sigmoid(z):
    s = 1 / (1 + np.exp(-z))
    return s

#Fuction for feedforward propagation
def forward_propagation(input_vector, weights_vector):
    W1, W2, W3 = splice_weights(weights_vector)

    #Neural network feed forward
    T0 = np.matmul(W1, input_vector.T)
    T1 = np.tanh(T0)
    T2 = np.matmul(W2, T1)
    T3 = np.tanh(T2)
    T4 = np.matmul(W3, T3)
    T5 = sigmoid(T4)
    return np.argmax(T5)
