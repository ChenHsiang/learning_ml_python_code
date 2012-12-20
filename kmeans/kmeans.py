
from time import time
import numpy as np
import pylab as pl
import codecs
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.cluster import spectral_clustering
import numpy as np
f = open("abd.txt",'r')
data = np.loadtxt(f)
X = data[:,:]  # select columns 1 through end
data = scale(X)
data = data*10
n_samples, n_features = data.shape
num_k=5
def bench_k_means(estimator, name, data):
    t0 = time()
    return estimator.fit_predict(data)

def ConvertCN(s):  
    return s

pca = PCA(n_components=6).fit(data)
label=bench_k_means(KMeans(init=pca.components_, n_clusters=6, n_init=1),
              name="PCA-based",
              data=data)

name=[]
dataa=data
ff=open("asd.txt")
data = ff.readline()
while(data):
    if data[:3] == codecs.BOM_UTF8:
        data = data[3:]
    name.append(data.decode("utf-8"))
    data = ff.readline()
news=dict(zip(name,dataa));

new_dict = dict(zip(name, label))
for a in new_dict:
    if new_dict[a]==5:
        print a[:-1]," ",new_dict[a]

