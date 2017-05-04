'''
Created on Mar 30, 2012
@author: Mujtaba Badat
'''

from __future__ import division
import numpy as np
import pylab as pl

'''
Helper class to remove rows/columns from sparsed matrix
I did not write this part; I got it from the internet (posted on stack overflow)
Created on Apr 2, 2012
@author: Justin Peel
http://stackoverflow.com/questions/2368544/how-can-i-remove-a-column-from-a-sparse-matrix-efficiently
'''
from scipy import sparse
from bisect import bisect_left

class lil2(sparse.lil_matrix):
    def removecol(self,j):
        if j < 0:
            j += self.shape[1]

        if j < 0 or j >= self.shape[1]:
            raise IndexError('column index out of bounds. Shape is ' + str(self.shape[1]))

        rows = self.rows
        data = self.data
        for i in xrange(self.shape[0]):
            pos = bisect_left(rows[i], j)
            if pos == len(rows[i]):
                continue
            elif rows[i][pos] == j:
                rows[i].pop(pos)
                data[i].pop(pos)
                if pos == len(rows[i]):
                    continue
            for pos2 in xrange(pos,len(rows[i])):
                rows[i][pos2] -= 1

        self._shape = (self._shape[0],self._shape[1]-1)
        
    def removerow(self,i):
        if i < 0:
            i += self.shape[0]

        if i < 0 or i >= self.shape[0]:
            raise IndexError('row index out of bounds')

        self.rows = np.delete(self.rows,i,0)
        self.data = np.delete(self.data,i,0)
        self._shape = (self._shape[0]-1,self.shape[1])

class Classifier ( object ):
    def __init__ ( self ):
        # initialization
        self.params = []
    
    def fit ( self, X, y ):
        # fitting the data
        raise NotImplementedError
    
    def predict ( self , X ):
        raise NotImplementedError
    
    def save_params ( self , fname ):
        params = dict ([( p , getattr ( self, p )) for p in self.params ])
        np.savez( fname, **params )
    
    def load_params ( self, fname ):
        params = np.load( fname )
        for name in self.params:
            setattr ( self, name, params[ name ])  

class MyClassifier(Classifier):
    '''
    classdocs
    
    N = number of data points to learn from
    n = sample size
    
    y_hat = sample response variable
    
    '''
    num_sentiments = 2   
        
    def __init__(self):
        # logpi is vector of prior probabilites for features being present when happy
        # logtheta is vector of observed probabilties for features being present when happy
        self.params = ['logpi', 'logtheta', 'feature_blacklist']
        
        
    def fit(self, X, y):
        num_sentiments = 2
        num_tweets,num_features = X.shape
        num_happy_tweets = np.sum(y)
        num_sad_tweets = num_tweets-num_happy_tweets
        self.feature_blacklist = []
        
        print "num_tweets " + str(num_tweets)
        print "num_features " + str(num_features)
        print "num_happy_tweets " + str(num_happy_tweets)
        print "num_sad_tweets " + str(num_sad_tweets)
        
        pi = [num_sad_tweets/num_tweets, num_happy_tweets/num_tweets]
        print "pi is " + str(pi)
        
        # self.logpi = [pi_0, pi_1]
        self.logpi = [np.log(num_sad_tweets/num_tweets), np.log(num_happy_tweets/num_tweets)]
        
        print "logpi: " + str(self.logpi)
        
        #theta
        #theta = np.array([((1-y)*X+1)/num_sad_tweets, ((y*X)+1)/num_happy_tweets])
        #delta_theta = abs(theta[0,:]-theta[1,:])
        #pl.plot(delta_theta)
        #pl.show()
                  
        self.logtheta = np.log(np.array([((1-y)*X+1)/(num_sad_tweets+2), ((y*X)+1)/(num_happy_tweets+2)]))
        
        print "logtheta" + str(self.logtheta)
        print self.logtheta.shape
        
        #information_gain = np.zeros((num_features, 1))
        
        #print sum(self.logtheta[0])
        #print sum(self.logtheta[1])
        ''' 
        for i in range(0, num_features-1):
            feature_given_0 = (1-y)*X[:,i]
            feature_given_1 = y*X[:,i]
            feature_freq = X[:,i].sum()
            #print "index " + str(i)
            
            #print feature_given_0
            #print feature_given_1
            #print feature_freq
            #print "break"
                       
            if feature_freq > 0:
                #print (feature_given_0/num_tweets)*np.log((feature_given_0/feature_freq)/pi[0])
                #print ((num_sad_tweets-feature_given_0)/num_tweets)*np.log(((num_sad_tweets-feature_given_0)/(num_tweets-feature_freq))/pi[0])
                if feature_given_0 > 0:
                    information_gain_0 = (feature_given_0/num_tweets)*np.log((feature_given_0/feature_freq)/pi[0]) + ((num_sad_tweets-feature_given_0)/num_tweets)*np.log(((num_sad_tweets-feature_given_0)/(num_tweets-feature_freq))/pi[0])
                if feature_given_1 > 1:
                    information_gain_1 = (feature_given_1/num_tweets)*np.log((feature_given_1/feature_freq)/pi[1]) + ((num_happy_tweets-feature_given_1)/num_tweets)*np.log(((num_happy_tweets-feature_given_1)/(num_tweets-feature_freq))/pi[1])
            
#                print information_gain_0
#                print information_gain_1
#                print "end"
                
                information_gain[i] = information_gain_0 + information_gain_1
            else:
                information_gain[i] = 0
                
            
            if information_gain[i] == 0:
                self.logtheta[0, i] = 0
                self.logtheta[1, i] = 0
        '''       
        #print sum(self.logtheta[0])
        #print sum(self.logtheta[1])
        #print information_gain.flatten()
        #print sum(information_gain) 
        
        
        '''        
        delta_theta = abs(np.log(((1-y)*X+1)/num_sad_tweets)-np.log(((y*X)+1)/num_happy_tweets))
        
        max_delta_theta = max(delta_theta)
        blacklist_threshold = .00005
        
        X = lil2(X)
        
        for i in range(0, num_features-1):
            if delta_theta[i] < blacklist_threshold:
                self.feature_blacklist.append(i)
        
        print self.feature_blacklist
        print len(self.feature_blacklist)
        '''
                
        #print "logpi is " + str(self.logpi)
        #print "logtheta is " + str(self.logtheta)

    def predict(self, X):
        n,num_features = X.shape
        y_hat = np.zeros((1,n))
        
        #print sum(self.logtheta[0,:])
        #print sum(self.logtheta[1,:])
        
        for i in range(n):
            x_i = np.array(X[i,:].todense()).flatten()
            
            L_i0 = self.logpi[0] + (np.dot((1-x_i), self.logtheta[0,:]))
            L_i1 = self.logpi[1] + np.dot(x_i, self.logtheta[1,:])
            
            #print "L_i0 " + str(L_i0)
            #print "L_i1 " + str(L_i1)
            
            log_sum_exp = np.logaddexp(L_i0, L_i1)
            
            p_i0 = np.exp(L_i0 - log_sum_exp)
            p_i1 = np.exp(L_i1 - log_sum_exp)
            
            if p_i0 > p_i1:
                y_hat[0, i] = 0
            else:
                y_hat[0, i] = 1
               
        return y_hat.flatten()
        