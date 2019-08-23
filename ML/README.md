# calML
Deriving Ca2+ Charge in Varying Environment Using Machine Learning Methods

## Machine Learning

_Data_: coordinates of the selected 70 loop3 structure from holoCaM from Pengzhi Zhang

Read all comments in the scripts themselves for formatting and input instructions.

Calcium charge is in the last column

__Data Manipulation__

* __Distancefromcoordinate.m__: Takes in coordinates, spits out Euclidean distance from the calcium ion

* __AddDistancetoCoordinates.m__: Takes in coordinate/Euclidean distance and spits out a 5-concatenation of atom number, x, y, z coordinates, and Euclidean distance

* __Clustering.m__: Takes in any format with charge in the last column and splits the data into positively and negatively charged sets

* __waterorientation.m__: Takes in point+distance from AddDistancetoCoordinates. Adds a binary feature based on the orientation of the water molecule: 1 if O is towards the calcium, 0 if away. Requires very specific formatting.


__Python Modeling__

All scripts only need to have the input files replaced. Training data and prediction data can be loaded at will. 

* __chickentester.py__: named for the chicken calmodulin’s calcium charge originally predicted by the script, but works on any set of training and prediction data. Input training data into train and data to be predicted into predict

* __Deeplearn.py__: training into train, prediction data into test. Uses H2O deep learning instead of random forest

* __ML.py__: originally written by PZ, it outputs variable importance. Only takes training data into class_df which is split randomly for validation.

* __MLnew.py__: takes in only training data into train, randomly splitting the set and outputting the validation predictions as numbers as well as presenting a few statistics

* __PabloML.py__: Written by Professor Pablo Rondon, this uses scikit learn random forest regressor from data loaded into filename

None of these scripts seem superior to the other, as the performance is largely dependent on the input data set. They are all thrown together for different outputs and analysis. 

Chickentester averages 100 models predictions, for example.
