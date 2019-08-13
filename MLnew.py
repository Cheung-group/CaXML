#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 14:36:40 2019

@author: nate
"""
import random
import h2o 
h2o.init()

output_path = "/home/nate/Desktop/"
train = '/home/nate/Desktop/MachineLearning/Realtests/distance(forrealmodels).txt'



class_df = h2o.import_file(train,sep=",")
X = class_df.col_names[:-1]
Y = class_df.col_names[-1]
testsize = 0.06
training, valid= class_df.split_frame([1-testsize], seed=random.randrange(1,999999999,1))

drf = h2o.estimators.H2ORandomForestEstimator()
drf.train(x=X, y=Y, training_frame=training, validation_frame=valid)
drf.model_performance()
pred = drf.predict(valid)

print(h2o.as_list(valid))

#Print Prediction as python list
print(h2o.as_list(pred[0]))

Error = drf.rmse(valid=True)
print("Error:")
print(Error)
Chargedf = h2o.as_list(valid[Y])
meanvalue = Chargedf['Cach'].mean()
ProportionError = Error/meanvalue
print("ProportionError:")
print(ProportionError)
###########
#MAKEPLOTS#
###########
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

import matplotlib.pyplot as plt


import seaborn as sns
sns.set(style='whitegrid',
        rc={'lines.linewidth': 2.5,
        'figure.figsize': (10, 8),
        'text.usetex': False,
        # 'font.family': 'sans-serif',
        # 'font.sans-serif': 'Optima LT Std',
        })

from pandas import set_option
set_option("display.max_rows", 10)
pd.options.mode.chained_assignment = None

# Plot outputs
import pylab as pl

#matplotlib inline
pl.plot((h2o.as_list(pred[0])), Chargedf,'ro')
pl.plot([0,5],[0,5], 'g-')
pl.xlabel('pred')
pl.ylabel('Charge')
pl.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, int(72*testsize +3))
ax.set_ylim(0, 5)
plt.plot(Chargedf, color='red')
plt.title("Charge")
plt.legend();

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, int(72*testsize +3))
ax.set_ylim(0, 5)
plt.plot(h2o.as_list(pred[0]), color='blue')
plt.title("RF (Predictions)")
plt.legend();

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, int(72*(testsize) +3))
ax.set_ylim(0, 5)
plt.plot(Chargedf, color='red', label = 'Charge')
plt.plot(h2o.as_list(pred[0]), color='blue', label = 'Predictions')
plt.legend(loc='best')
plt.show()



from sklearn.metrics import r2_score
r2score = (r2_score(Chargedf, h2o.as_list(pred[0])))
print(r2score)

from scipy.stats.stats import pearsonr
pearsonrscore=(pearsonr(Chargedf, h2o.as_list(pred[0])))
print(pearsonrscore)

#with open('/home/nate/Desktop/posperformancedata.txt', 'a+') as f:
   # print(h2o.as_list(pred[0]).values.tolist(), Chargedf.values.tolist(), Error, ProportionError, r2score, pearsonrscore, file=f, sep=',')