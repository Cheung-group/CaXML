#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 15:24:45 2019

@author: nate
"""

import h2o
h2o.init()

output_path = "/home/nate/Desktop/"
predict = '/home/nate/Desktop/negative.txt'
train = '/home/nate/Desktop/MachineLearning/Realtests/distance(forrealmodels).txt'



class_df = h2o.import_file(train,sep=",")
valid = h2o.import_file(predict,sep=",")
X = class_df.col_names[:-1]
Y = class_df.col_names[-1]


counter=1
while counter<=100:
    drf = h2o.estimators.H2ORandomForestEstimator()
    drf.train(x=X, y=Y, training_frame=class_df, validation_frame=valid)
    drf.model_performance()
    pred = drf.predict(valid)

#print(h2o.as_list(valid))

#Print Prediction as python list
    print(h2o.as_list(pred[0]))






    with open('/home/nate/Desktop/SplicePerformance.txt', 'a+') as f:
        print(h2o.as_list(pred[0]).values.tolist(), file=f, sep=',')


    counter+=1
