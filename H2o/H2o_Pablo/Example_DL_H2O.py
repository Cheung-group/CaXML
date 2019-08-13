#!/usr/bin/env python
# coding: utf-8
# Load the H2O Python module.

import h2o

h2o.init()

# Start H2O
from h2o.estimators.deeplearning import H2OAutoEncoderEstimator, H2ODeepLearningEstimator

#get_ipython().magic(u'matplotlib inline')

#IMPORT ALL THE THINGS
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class_df = h2o.import_file("Data_Glioblatoma5Patients_SC.csv")

#split the data as described above
train, valid, test = class_df.split_frame([0.6, 0.2], seed=1234)

#Prepare predictors and response columns
class_X = class_df.col_names[:-1]     #last column is varibale to estimate,
class_y = class_df.col_names[-1]

# Encode the response column as categorical for multinomial classification
train[class_y] = train[class_y].asfactor()
test[class_y] = test[class_y].asfactor()


model = H2ODeepLearningEstimator(
   distribution="multinomial",
   activation="rectifier",
   loss = "cross entropy",
   stopping_metric="misclassification", ## alternatives: "MSE","logloss","r2"
   mini_batch_size=20,
   hidden=[250,250,250],                      ## for better generalization
   input_dropout_ratio=0.2,
   nfolds=3,
   epochs=1000,                            ## need more epochs for a better model
   variable_importances=True,
   standardize = True)

model.train(class_X, class_y, training_frame=train, validation_frame=valid)

model.scoring_history()

model.model_performance(train=True) # training metrics

model.model_performance(valid=True) # validation metrics

model.mean_per_class_error(valid=True)

predictions = model.predict(test)

predictions.describe()


# Retrieve the variable importance
import pandas as pd
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

