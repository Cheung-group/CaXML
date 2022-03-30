#!/usr/bin/env python
# coding: utf-8
# Load the H2O Python module.

import h2o
from h2o.estimators import H2ORandomForestEstimator as RFE

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


h2o.init()
class_df = h2o.import_file("data.txt",sep=",")

#split the data as described above
train, valid= class_df.split_frame([0.75], seed=1791)

#Prepare predictors and response columns
class_X = class_df.col_names[:-1]     #last column is varibale to estimate,
class_y = class_df.col_names[-1]

model = RFE(ntrees=100, max_depth=20, nfolds=10)
model.train(x=class_X, y=class_y, training_frame=train, validation_frame=valid)

model.scoring_history()
model.model_performance(train=True) # training metrics
model.model_performance(valid=True) # validation metrics

# Retrieve the variable importance
pd.DataFrame(model.varimp())
var_df = pd.DataFrame(model.varimp(),
             columns=["Variable", "Relative Importance", "Scaled Importance", "Percentage"])
print (var_df.shape)
var_df.head(10)

model.varimp_plot(num_of_features=10)

plt.rcdefaults()
fig, ax = plt.subplots()
variables = model._model_json['output']['variable_importances']['variable']
y_pos = np.arange(len(variables))
scaled_importance = model._model_json['output']['variable_importances']['scaled_importance']
ax.barh(y_pos, scaled_importance, align='center', color='green', ecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(variables)
ax.invert_yaxis()
ax.set_xlabel('Scaled Importance')
ax.set_title('Variable Importance')
plt.show()

