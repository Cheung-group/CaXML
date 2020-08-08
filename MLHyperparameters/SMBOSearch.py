# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 14:50:51 2020

@author: illum
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import skopt
from skopt.utils import use_named_args
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPRegressor

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

#csv file with features in each column and a target regression column with title 'Cachg'
filename = 'C:/Users/illum/Desktop/UH Research/Machine Learning/graphtheorydata.csv' #Change for different datasets
data = pd.read_csv(filename, sep=',')

x = pd.DataFrame(data)
y = pd.DataFrame(data.Cachg) #Change to title of target regression column

#Prepare predictors and response columns

correct_Pattern_labels = data['Cachg'].values #Change to title of target regression column
feature_vectors = data.drop(['Cachg'], axis=1) #Change to title of target regression column


testsize = 0.05
rstate = random.randrange(1,999999999,1)
X_train, X_test, y_train, y_test = train_test_split(feature_vectors, correct_Pattern_labels, test_size = testsize, random_state = rstate)

scaler = preprocessing.MinMaxScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

#The space of hyperparameters to search
parameter_grid=[skopt.space.Categorical(['tanh', 'relu','logistic'],name='activation'),
skopt.space.Categorical(['lbfgs','adam','sgd'],name='solver'),
skopt.space.Real(10**-5,10**1,"log-uniform",name='alpha'), 
skopt.space.Categorical(['adaptive','constant','invscaling'],name='learning_rate'),
skopt.space.Real(10**-3,10**0,name='learning_rate_init'),
skopt.space.Real(-2.5,2.5,name='power_t'),
skopt.space.Categorical([10000],name='max_iter'),
skopt.space.Categorical([0.01],name='tol'),
skopt.space.Real(0,0.8,name='momentum'),
skopt.space.Categorical([True],name='early_stopping'),
skopt.space.Integer(15,25,name='hidden_layer_sizes')]

@use_named_args(parameter_grid)

#Score defaults to the negative cross-evaluated default score of the model
def ScoreFunction(**hyperparameters):   
    estimator = MLPRegressor(**hyperparameters)
    cvscore = cross_val_score(estimator,X_train,(y_train-y_train.mean())/y_train.std(),cv=5)
    score = -1*cvscore.mean()
    return score

#Load previous results
with open("reduceddataresults.txt","rb") as file:
    previousresults = pickle.load(file)
with open("reduceddatascores.txt","rb") as file:
  previousscores=pickle.load(file)

#SMBO training
scorereport=skopt.gp_minimize(ScoreFunction,parameter_grid,n_calls=0,random_state=1,acq_func='EI',n_random_starts=0,verbose=True, x0=previousresults,y0=previousscores)

#Best training results
print('Best Validation=%.4f' %scorereport.fun)
print('Best Hyperparameters:')
print(scorereport.x)

#Store results
with open("reduceddataresults.txt","wb") as file:
    pickle.dump(scorereport.x_iters,file)
with open("reduceddatascores.txt","wb") as file:
    pickle.dump(scorereport.func_vals,file)

#Convergence plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, len(scorereport.func_vals))
ax.set_ylim(-0.3, 0.3)
plt.scatter(range(len(scorereport.func_vals)), scorereport.func_vals)
plt.show()

#Feature Importances
hyperparameters=dict(zip(['activation','solver','alpha','learning_rate','learning_rate_init','power_t','max_iter','tol','momentum','early_stopping','hidden_layer_sizes'],scorereport.x))

Regressor=MLPRegressor(**hyperparameters)
Regressor.fit(X_train,(y_train-y_train.mean())/y_train.std())
predtest=Regressor.predict(X_test)
baseline=Regressor.score(X_test,(y_test-y_train.mean())/y_train.std())

importances=[]
Features=pd.DataFrame(X_train.copy())
for n in range(X_train.shape[1]):
    X_train=np.asarray(Features).copy()
    np.random.shuffle(X_train[:,n])
    Regressor.fit(X_train,(y_train-y_train.mean())/y_train.std())
    rsquaredtest=Regressor.score(X_test,(y_test-y_train.mean())/y_train.std())
    importances.append(rsquaredtest)

#Plot Importances
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, X_train.shape[1])
ax.set_ylim(-5, 50)
trueimportances=(baseline-np.asarray(importances))*100
plt.bar(list(range(X_train.shape[1])), trueimportances)
plt.show()

#Find names of the important features
truefeatures=[]
for n in range(len(importances)):
    if trueimportances[n]>0:
        truefeatures.append(n)
truedatafeatures=[data.columns[index] for index in truefeatures]