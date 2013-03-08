#Filename logistic_regression.py
from numpy import *
from pylab import *
import matplotlib.pyplot as plt

#the sigmoid function return sigmoid_value of every elements in array
def sigmoid(x):
    def sigm(t):
      return 1.0/(1+e**(-t));
    unf=frompyfunc(sigm, 1, 1)
    #y=unf(x).astype(float);
    return unf(x);




X=matrix([[1,1],[1,2],[1,3],[1,4],[1,5],[1,6]]);
print sigmoid(2)
