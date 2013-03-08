#Filename liner_regression.py
from numpy import *
from pylab import *
import matplotlib.pyplot as plt

#simple regression using the matrix way
def fit(X,y):
    return inv(X.T*X)*X.T*y;


#simple regression using the gradient descent way
def gradientDescent(X, y, theta, alpha, num_iters=50):
    m=len(y)
    for iter in range(1,num_iters+1):
        q=(X*theta-y);
        theta=theta-alpha/m*X.T*q
    return theta

#ridge regression using the gradient descent way
def gradientDescentWithP(X, y, theta, alpha,lambdas, num_iters=50):
    m=len(y)
    for iter in range(1,num_iters+1):
        q=(X*theta-y);
        grad=X.T*q/m+(lambdas/m)*theta
        gradd=X.T*q/m
        grad[0]=gradd[0]
        theta=theta-alpha*grad
    return theta

#ridge regression using the matrix way
def fitWithP(X,y,lambdas):
    return (inv(lambdas*eye(X.shape[1])+X.T*y)*X.T*y)

X=matrix([
[1,1.7611110925674438],
[1,2.7111110925674438],
[1,4.311111092567444],
[1,5.211111092567444],
[1,6.4111110925674435],
[1,7.761111092567444],
[1,9.111111092567445],
[1,10.211111092567444],
[1,12.861111092567445],
[1,14.311111092567444],
[1,16.661111092567445],
[1,17.861111092567445],
[1,19.011111092567443],
[1,20.161111092567445],
[1,22.711111092567442],
[1,23.711111092567442],
[1,26.161111092567445],
[1,27.261111092567443],
[1,28.261111092567443],
[1,30.111111092567445],
[1,24.411111092567445],
[1,20.461111092567442],
[1,21.711111092567442],
[1,20.811111092567444],
[1,10.511111092567443]]);

y=arange(1,7).reshape((6,1))
y[5]=1;
y=[
[1.6876739501953124],
[2.2876739501953125],
[2.6876739501953124],
[2.6876739501953124],
[3.0876739501953123],
[3.9876739501953127],
[4.7876739501953125],
[5.587673950195312],
[5.987673950195313],
[5.737673950195313],
[6.337673950195312],
[7.237673950195313],
[8.187673950195313],
[9.137673950195312],
[10.137673950195312],
[10.137673950195312],
[10.337673950195313],
[10.737673950195312],
[11.787673950195312],
[12.837673950195313],
[10.237673950195312],
[9.987673950195312],
[9.537673950195312],
[8.787673950195312],
[4.687673950195313]]
print y
plt.plot(X[:,1],y,'o')
theta = zeros((2,1))
iterations = 3500
alpha = 0.01
#theta = gradientDescent(X, y, theta, alpha, iterations);
theta = fit(X,y)
#theta = gradientDescentWithP(X, y, theta, alpha,10, iterations);
#theta = fitWithP(X,y,10)
print theta
xx = linspace(0, 35, 6)
a=theta[0];
b=theta[1];
def fun(x):
    return a+b*x;
unf=frompyfunc(fun, 1, 1)
yy =unf(xx).astype(float);
print yy
plt.plot(xx,yy)
plt.show()
