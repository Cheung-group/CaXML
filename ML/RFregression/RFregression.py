import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import random
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import sklearn.metrics as sm
from sklearn.preprocessing import scale
from sklearn import cluster
from sklearn import metrics


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

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from scipy.stats import truncnorm

from sklearn.ensemble import RandomForestClassifier

filename = './data.txt'
data = pd.read_csv(filename)
data



x = pd.DataFrame(data)
#Prepare predictors and response columns

#x = pd.DataFrame(data, columns=['Type','x', 'y', 'z', 'Charge'])

#x = pd.DataFrame(data, columns=['C1Ca','C2Ca','C3Ca','O4Ca','O5Ca','C6Ca',
#'C7Ca','C8Ca','O9Ca','O10Ca','C11Ca','C12Ca','C13Ca','C14Ca','O15Ca','O16Ca',
#'Cach'])
#'C1','C1x','C1y','C1z','C1Ca','C2','C2x','C2y','C2z','C2Ca','C3',
#'C3x','C3y','C3z','C3Ca','O4','O4x','O4y','O4z','O4Ca','O5','O5x',
#'O5y','O5z','O5Ca','H6','H6x','H6y','H6z','H6Ca','H7','H7x','H7y',
#'H7z','H7Ca','H8','H8x','H8y','H8z','H8Ca','H9','H9x','H9y','H9z',
#'H9Ca','H10','H10x','H10y','H10z','H10Ca','H11','H11x','H11y','H11z',
#'H11Ca','C12','C12x','C12y','C12z','C12Ca','C13','C13x','C13y','C13z',
#'C13Ca','C14','C14x','C14y','C14z','C14Ca','O15','O15x','O15y','O15z',
#'O15Ca','O16','O16x','O16y','O16z','O16Ca','H17','H17x','H17y','H17z',
#'H17Ca','H18','H18x','H18y','H18z','H18Ca','H19','H19x','H19y','H19z',
#'H19Ca','H20','H20x','H20y','H20z','H20Ca','H21','H21x','H21','H21z',
#'H21Ca','C22','C22x','C22y','C22z','C22Ca','C23','C23x','C23y','C23z',
#'C23Ca','C24','C24x','C24y','C24z','C24Ca','C25','C25x','C25y','C25z',
#'C25Ca','O26','O26x','O26y','O26z','O26Ca','O27','O27x','O27y','O27z',
#'O27Ca','H28','H28x','H28y','H28z','H28Ca','H29','H29x','H29y','H29z',
#'H29C','H30','H30x','H30y','H30z','H30Ca','H31','H31x','H31y','H31z',
#'H31Ca','H32','H32x','H32y','H32z','H32Ca','H33','H33x','H33y','H33z',
#'H33Ca','H34','H34x','H34y','H34z','H34Ca','Ca35','Ca35x','Ca35y','Ca35z',
#'Ca35Ca','O36','O36x','O36y','O36z','O36Ca','H37','H37x','H37y','H37z',
#'H37Ca','H38','H38x','H38y','H38z','H38Ca','H2OOreintation'])

y = pd.DataFrame(data.Cachg)

correct_Pattern_labels = data['Cachg'].values

feature_vectors = data.drop(['Cachg'], axis=1)

feature_vectors.describe()



from sklearn.ensemble import RandomForestRegressor

scaler = preprocessing.StandardScaler().fit(feature_vectors)
scaled_features = scaler.transform(feature_vectors)

#X_train, X_test, y_train, y_test = train_test_split(
testsize = 0.1
X_train, X_test, y_train, y_test = train_test_split(feature_vectors,
correct_Pattern_labels, test_size=testsize,
random_state=random.randrange(1,999999999,1))

# Estimate the score on the entire dataset, with no missing values
estimator = RandomForestRegressor(random_state=random.randrange(1,999999999,1),
n_estimators=10000, n_jobs=10)
estimator.fit(X_train, y_train)
pred = estimator.predict(X_test)

from sklearn.model_selection import cross_val_score
score = cross_val_score(estimator, X_train, y_train).mean()
print("Score with the entire dataset = %.2f" % score)

y_test1 = np.asarray(y_test)


# Plot outputs
import pylab as pl
#matplotlib inline
pl.plot(pred, y_test,'ro')
pl.plot([1,3],[1,3], 'g-')
pl.xlabel('Predicted charge')
pl.ylabel('QM charge')
pl.show()

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set_xlim(0, int(72*testsize +4))
#ax.set_ylim(1, 3)
#plt.plot(y_test1, color='red')
#plt.title("Charge")
#plt.legend();

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set_xlim(0, int(72*testsize +4))
#ax.set_ylim(1, 3)
#plt.plot(pred, color='blue')
#plt.title("RF (Predictions)")
#plt.legend();

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, int(72*testsize +3))
ax.set_ylim(1, 3)
plt.plot(y_test1, color='red', label = 'QM charge')
plt.plot(pred, color='blue', label = 'Predicted charge')
plt.legend(loc='best')
plt.show()


from sklearn.metrics import r2_score
print(r2_score(y_test1, pred))


from scipy.stats.stats import pearsonr
print(pearsonr(y_test1, pred))

importances = estimator.feature_importances_


std = np.std([tree.feature_importances_ for tree in estimator.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(X_train.shape[1]):
    print("%d. feature %s (%f)" % (f + 1, X_train.axes[1][indices[f]], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(X_train.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X_train.shape[1]), indices)
plt.xlim([-1, X_train.shape[1]])
plt.show()
