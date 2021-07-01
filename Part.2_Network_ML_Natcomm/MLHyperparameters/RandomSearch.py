# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:35:00 2020

@author: illum
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:19:01 2020

@author: Nate Jennings
"""

import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split


filename = 'C:/Users/illum/Desktop/UH Research/Machine Learning/graphtheorydata.csv' #Change for different data
data = pd.read_csv(filename, sep=',')

x = pd.DataFrame(data) #All data: Each row is a frame of data with features in each column and the charge to predict in the last column
y = pd.DataFrame(data.Cachg) #Charges to predict

#Prepare predictors and response columns

correct_Pattern_labels = data['Cachg'].values #Predictors
feature_vectors = data.drop(['Cachg'], axis=1) #Response

from sklearn.neural_network import MLPRegressor

testsize = 0.05
rstate = random.randrange(1,999999999,1)
X_train, X_test, y_train, y_test = train_test_split(feature_vectors, correct_Pattern_labels, test_size = testsize, random_state = rstate)


from sklearn.model_selection import cross_val_score

#Default score is the cross-evaluated default score of the model.
def ScoreFunction(hyperparameters,iteration):
    estimator=MLPRegressor(**hyperparameters)
    cvscore = cross_val_score(estimator,X_train,y_train,cv=5)
    score = cvscore.mean()
    return [score, hyperparameters,iteration]


#Domain of hyperparameter search
tens=10*np.ones((100000,))    
logalpha=np.asarray([]) #alpha uniformly distributed in its log
loglearningrateinit=np.asarray([]) #uniform in log
powert=np.asarray([]) #uniform
logmomentum=np.asarray([]) #uniform in log
for v in range(0,100000):
    logalpha=np.append(logalpha,random.uniform(-5,1))
    loglearningrateinit=np.append(loglearningrateinit,random.uniform(-3,0))
    powert=np.append(powert,random.uniform(-2.5,2.5))
    logmomentum=np.append(logmomentum,random.uniform(-3,0))
alpha=np.power(tens,logalpha)
learningrateinit=np.power(tens,loglearningrateinit)
momentum=np.power(tens,logmomentum)

#Space of hyperparameters to search through
parameter_grid={'activation':['logistic','tanh','relu'],
'solver':['lbfgs','sgd','adam'],
'alpha':np.ndarray.tolist(alpha),
'learning_rate':['constant','invscaling','adaptive'],
'learning_rate_init':np.ndarray.tolist(learningrateinit),
'power_t':np.ndarray.tolist(powert),
'max_iter':[10000],
'tol':[0.01],
'momentum':np.ndarray.tolist(momentum),
'early_stopping':[True],
'hidden_layer_sizes':[21]}



#Hyperparameter random search tuning


MAX_EVAL=1 #Number of random searches
def random_search(parameter_grid):
    testing_results=pd.DataFrame(columns=['score','hyperparameters','iter'],
                                 index=list(range(MAX_EVAL)))
    for i in range(MAX_EVAL):
        hyperparameters={k:random.sample(v,1)[0] for k, v in parameter_grid.items()}
        eval_results=ScoreFunction(hyperparameters,i)
        testing_results.loc[i,:]=eval_results
    testing_results.sort_values('score',ascending=False,inplace=True)
    testing_results.reset_index(inplace=True)
    return testing_results
random_results=random_search(parameter_grid)


print('Best validation: {:.5f}'.format(random_results.loc[0,'score']))
import pprint
print('Best hyperparameters:')
pprint.pprint(random_results.loc[0,'hyperparameters'])
#Random_results=open("Random Results","a")
#Random_results.write(random_results.to_string())
#Random_results.close()

