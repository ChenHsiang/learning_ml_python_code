# naive bayes classifier program with BernoulliNB
import numpy as np
import math
import re
from sklearn.naive_bayes import BernoulliNB

def getwords(doc):
    splitter=re.compile('\\W*')
    words=[s.lower() for s in splitter.split(doc)
           if len(s)>2 and len(s)<20]
    return dict((w,1) for w in words)    

data={'Nobody owns the water.':'good',\
'the quick rabbit jumps fences':'good'\
,'buy pharmaceuticals now':'bad'\
,'make quick money at the online casino':'bad'\
,'the quick brown fox jumps':'good'}
s=""
for x in data:
    s+=" "+x
feature=getwords(s);
bin_data=[];

def getfeatures(doc):
    words=getwords(doc)
    global feature
    bin_data=[]
    for f in feature:
            if f in words:
                bin_data.append(1)
            else:
                bin_data.append(0)
    return bin_data



for x in data:
    for f in feature:
        if f in x:
            bin_data.append(1)
        else:
            bin_data.append(0)
            
#print len(feature)
#print s
#print len(bin_data)
X=np.array(bin_data)
X=X.reshape(len(data),len(feature))
#print X
Y=[]
for  x in data:
    if data[x]=='good':
        Y.append(1)
    else:
        Y.append(0)


clf = BernoulliNB()
clf.fit(X, Y)
print clf.predict(getfeatures('quick rabbit'))
