import numpy as np
from utils import *

# global pre computations
XTX = None
XTY = None

def preprocess(X, Y):
	''' TASK 0
	X = input feature matrix [N X D] 
	Y = output values [N X 1]
	Convert data X, Y obtained from read_data() to a usable format by gradient descent function
	Return the processed X, Y that can be directly passed to grad_descent function
	NOTE: X has first column denote index of data point. Ignore that column 
	and add constant 1 instead (for bias part of feature set)
	'''

	X_ = np.ones((X.shape[0],1))

	for i in range(1,X.shape[1]):

		if type(X[0][i]) != type("string"): # float or integer
			Mean = np.mean(X[:,i], 0)
			Std = (X[:,i]-Mean)**2
			Std = np.sqrt(np.mean(Std,0))
			X[:,i] -= Mean
			X[:,i] /= Std
			X_ = np.append(X_,X[:,i].reshape(-1,1),1)

		else:
			labels = np.unique(X[:,i]) # string
			X_ = np.append(X_, one_hot_encode(X[:,i], labels),1)

	print(X_.shape)
	X_ = X_.astype('float64')
	Y = Y.astype('float64')
	return X_, Y

def grad_ridge(W, X, Y, _lambda):
	'''  TASK 2
	W = weight vector [D X 1]
	X = input feature matrix [N X D]
	Y = output values [N X 1]
	_lambda = scalar parameter lambda
	Return the gradient of ridge objective function (||Y - X W||^2  + lambda*||w||^2 )
	'''
	grad = None
	if XTX is None:
		grad = 2.0 * (np.matmul(np.matmul(X.T,X), W) - np.matmul(X.T,Y) + (_lambda * W))
	else:
		grad = 2.0 * (np.matmul(XTX, W) - XTY + (_lambda * W))
	return grad

def ridge_grad_descent(X, Y, _lambda, max_iter=30000, lr=0.00017, epsilon = 1e-2):
	''' TASK 2
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	_lambda 	= scalar parameter lambda
	max_iter 	= maximum number of iterations of gradient descent to run in case of no convergence
	lr 			= learning rate
	epsilon 	= gradient norm below which we can say that the algorithm has converged 
	Return the trained weight vector [D X 1] after performing gradient descent using Ridge Loss Function 
	NOTE: You may precompure some values to make computation faster
	'''

	XTX = np.matmul(X.T,X)
	XTY = np.matmul(X.T,Y)

	W = np.zeros((X.shape[1],1))

	for epoch in range(max_iter):

		grad = grad_ridge(W, X, Y, _lambda)
		if np.linalg.norm(grad) < epsilon:
			break
		W -= lr * grad

	XTX = None
	XTY = None

	return W

def k_fold_cross_validation(X, Y, k, lambdas, algo):
	''' TASK 3
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	k 			= number of splits to perform while doing kfold cross validation
	lambdas 	= list of scalar parameter lambda
	algo 		= one of {coord_grad_descent, ridge_grad_descent}
	Return a list of average SSE values (on validation set) across various datasets obtained from k equal splits in X, Y 
	on each of the lambdas given 
	'''

	split_size = Y.shape[0]//k
	avg_sse = []
	for _lambda in lambdas:
		sse_val = float(0)
		for i in range(k):
			X_ = np.append(X[:i*split_size,:],X[(i+1)*split_size:,:],0)
			Y_ = np.append(Y[:i*split_size,:],Y[(i+1)*split_size:,:],0)
			W = algo(X_,Y_,_lambda)
			sse_val += sse(X[(i*split_size):((i+1)*split_size),:],Y[(i*split_size):((i+1)*split_size),:],W)
		avg_sse.append(sse_val/float(k))
	return avg_sse



def coord_grad_descent(X, Y, _lambda, max_iter=2000):
	''' TASK 4
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	_lambda 	= scalar parameter lambda
	max_iter 	= maximum number of iterations of gradient descent to run in case of no convergence
	Return the trained weight vector [D X 1] after performing gradient descent using Ridge Loss Function 
	'''
	pass

if __name__ == "__main__":
	# Do your testing for Kfold Cross Validation in by experimenting with the code below 
	X, Y = read_data("./dataset/train.csv")
	X, Y = preprocess(X, Y)
	trainX, trainY, testX, testY = separate_data(X, Y)
	
	lambdas = [...] # Assign a suitable list Task 5 need best SSE on test data so tune lambda accordingly
	scores = k_fold_cross_validation(trainX, trainY, 6, lambdas, ridge_grad_descent)
	plot_kfold(lambdas. scores)