#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:08:55 2019

@author: nate
"""

import h2o
h2o.init()

train = 'data.txt'
#test = '/home/nate/Desktop/distancetest.txt'


class_df = h2o.import_file(train,sep=",")
#predictdata = h2o.import_file(test,sep=",")
X = class_df.col_names[:-1]
Y = class_df.col_names[-1]

training, valid, test = class_df.split_frame([0.8,0.1], seed=1234)

deep = h2o.estimators.H2ODeepLearningEstimator()
deep.train(x=X, y=Y, training_frame=training, validation_frame=valid)
deep.model_performance()
#"pred = deep.predict(predictdata)
pred = deep.predict(test)

#Print Prediction as python list
print(h2o.as_list(pred[0]))
