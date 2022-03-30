import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import random
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn import metrics

import seaborn as 
sns.set(style='whitegrid',
        rc={'lines.linewidth': 2.5,
        'figure.figsize': (10, 8),
        'text.usetex': False,
        #'font.family': 'sans-serif',
        #'font.sans-serif': 'Optima LT Std',
        })

from pandas import set_option
#set_option("display.max_rows", 10)
pd.options.mode.chained_assignment = None

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from scipy.stats import truncnorm
from sklearn.ensemble import RandomForestClassifier

filename = 'data.txt'
data = pd.read_csv(filename, sep=' ')

x = pd.DataFrame(data)
y = pd.DataFrame(data.Cachg)

#Prepare predictors and response columns

correct_Pattern_labels = data['Cachg'].values
feature_vectors = data.drop(['Cachg'], axis=1)
feature_vectors.describe()

from sklearn.ensemble import RandomForestRegressor

scaler = preprocessing.StandardScaler().fit(feature_vectors)
scaled_features = scaler.transform(feature_vectors)

testsize = 0.1
rstate = random.randrange(1,999999999,1)
X_train, X_test, y_train, y_test = train_test_split(feature_vectors, correct_Pattern_labels, test_size = testsize, random_state = rstate)

from sklearn.decomposition import PCA


#############################################################################
# Compute a PCA (anticlines) on the anticlines dataset (treated as unlabeled
# dataset): unsupervised feature extraction / dimensionality reduction
#from time import time
#n_components = 50

#t0 = time()
#pca = PCA(n_components=n_components, svd_solver='randomized',
#                   whiten=True).fit(X_train)
#print("done in %0.3fs" % (time() - t0))

#print("Projecting the input data on the eigen-anticlines orthonormal basis")
#t0 = time()
#X_train_pca = pca.transform(X_train)
#X_test_pca = pca.transform(X_test)
#print("done in %0.3fs" % (time() - t0))

#############################################################################

X_train_pca = X_train
X_test_pca = X_test

# Estimate the score on the entire dataset, with no missing values
rstate = random.randrange(1,999999999,1)
estimator = RandomForestRegressor(random_state = rstate, n_estimators = 500, n_jobs = 12)
estimator.fit(X_train_pca, y_train)
pred = estimator.predict(X_test_pca)

from sklearn.model_selection import cross_val_score
cvscore = cross_val_score(estimator, X_train, y_train, cv=5)
score = cvscore.mean()
print("Score with the entire dataset = %.2f" % score)

y_test1 = np.asarray(y_test)

# Plot outputs
import pylab as pl
pl.plot(pred, y_test,'ro')
pl.plot([1,3],[1,3], 'g-')
pl.xlabel('Predicted charge')
pl.ylabel('QM charge')
#pl.show()


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(0, int(72*testsize +3))
ax.set_ylim(1, 3)
plt.plot(y_test1, color='red', label = 'QM charge')
plt.plot(pred, color='blue', label = 'Predicted charge')
plt.legend(loc='best')
#plt.show()


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
#plt.show()
