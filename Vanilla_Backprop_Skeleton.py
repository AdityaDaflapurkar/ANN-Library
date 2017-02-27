import numpy as np
import random

class Perceptron:

    def __init__(self):
        self.hidden_layer_size = 4 # Change as per preferences
        self.alpha = 10 # Learning Rate
        np.random.seed(42)
        self.w0 = 2*np.random.random((3, self.hidden_layer_size)) - 1
        self.w1 = 2*np.random.random((self.hidden_layer_size + 1, 1)) - 1 # One more node as bias (4+1)

    def sigmoid(self, x, deriv=False):
        if deriv == True:
            return x*(1-x)
        return 1/(1+np.exp(-x))

    def train(self, X, Y, iterations):

        for iter in range(iterations):
		for row in X:	
        	    # Forward propagation
        	    l0 = X[row] # Input
        	    l1 = sigmoid(a[i],false) for i in a=np.dot(l0,self.w0) # Output from hidden layer (2nd layer)
        	    l1_with_bias = np.insert(l1,0,1,axis=1)# Stack 1's as first element of each training set
        	    l2 = sigmoid(np.dot(l1_with_bias,w1),false)# Output from final layer (3rd layer)
	
        	    # Backward propagation
        	    l2_error = Y-l2# Final error for each training set (Nx1 matrix)
        	    # To get average error in that batch, you may take the average of all elements in l2_error
        	    l2_delta = # Deltas for final layer, check formula
	
        	    l1_error = # Error for the hidden layer, check formula
        	    l1_delta = # Deltas for the hidden layer, check formula

        	    # Update weights w0 and w1 here

    def predict(self, X):
        y_pred = # Predict for a given dataset X
        return y_pred


if __name__ =='__main__':
    p = Perceptron()
    X = np.array([  [1,0,1],
                    [1,1,0],
                    [1,1,1],
                    [1,0,0]  ])

    y = np.array([  [1],
                    [1],
                    [0],
                    [0]  ])

    p.train(X, y, 1000)
    print(p.predict(np.array([  [1,1,1],
                                [1,0,0],
                                [1,0,1],
                                [1,1,0]  ])
                            ))
