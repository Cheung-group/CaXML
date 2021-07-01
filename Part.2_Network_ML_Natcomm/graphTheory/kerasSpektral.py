import tensorflow as tf
import numpy as np
import scipy
import pandas
import os
def analogous(n):
    translation = {}
    for num in [20,56,93,129]:
        for k in range(12):
            translation[num + k] = k + 1
    if n in [13,14,15,16]:
        return n
    return translation[n]

def contactMapToDict(contactFile):
    contactTable = pandas.read_csv(contactFile)
    allGraphs = {}
    rows = contactTable['Frame']
    frame = 0
    contactDict = contactDictInit()
    for row in range(len(rows)):
        if not rows[row] == frame:
            allGraphs[frame] = contactDict
            contactDict = contactDictInit()
            frame = rows[row]
        sourceNum = str(contactTable.iloc[row]['Source'])[-4:]
        sourceNum = analogous(int(sourceNum))
        targetNum = str(contactTable.iloc[row]['Target'])[-4:]
        targetNum = analogous(int(targetNum))
        if sourceNum in contactDict.keys():
            contactDict[sourceNum] = set(contactDict[sourceNum])
        else:
            contactDict[sourceNum] = set()
        contactDict[sourceNum].add(targetNum)
        contactDict[sourceNum] = list(contactDict[sourceNum])
        if row == len(rows)-1:
            allGraphs[frame] = contactDict
            contactDict = contactDictInit()
            frame = rows[row]
    return allGraphs
    
def contactDictInit():
    contactDict = {}
    for node in range(14):
        contactDict[node] = set([])
    return contactDict

def featureMatrices(featureFile):
    allFeatures = {}
    allLabels = {}
    featureTable = pandas.read_csv(featureFile)
    rows = featureTable.shape[0]
    columns = featureTable.columns
    charges = np.asarray(featureTable['Cachg'])
    for row in range(rows):
        allFeatures[row] = [[] for k in range(14)]
        for column in columns:
            node = largestNumFromLeft(column)
            if node:
                node = node - 1
                allFeatures[row][node] = allFeatures[row][node] + [featureTable.iloc[row][column]]
            if column == "Cachg":
                allLabels[row] = featureTable.iloc[row][column]
    for key in allFeatures.keys():
        allFeatures[key] = np.asarray(allFeatures[key])
    labels = labelsToOneHot(allLabels)
    return allFeatures,labels

def labelsToOneHot(dictionary):
    maxZ = max(dictionary.values())
    minZ = min(dictionary.values())
    eVPrecision = 0.01
    bins = 1/eVPrecision
    lengthOneHot = int((maxZ - minZ) * bins) + 1
    oneHotLabels = []
    for key in dictionary.keys():
        Z = dictionary[key]
        position = int((Z - minZ) * bins)
        oneHot = np.zeros((lengthOneHot,))
        oneHot[position] = 1
        oneHotLabels.append(oneHot)
    return oneHotLabels

def largestNumFromLeft(string):
    for i in range(len(string)):
        try:
            largestNum = int(string[:i+1])
        except ValueError:
            if i > 0:
                return largestNum
            else:
                return ''
    return largestNum

def dictToGraph(dictionary):
    keys = dictionary.keys()
    numNodes = max(keys)
    graph = np.zeros((numNodes,numNodes))
    for key in list(keys):
        for target in dictionary[key]:
            graph[key-1][target-1] = 1
    return scipy.sparse.csr.csr_matrix(graph)


from spektral.data import Dataset
from spektral.data.graph import Graph
class data2000(Dataset):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def download(self):
        featureFile = 'C:/Users/illum/Desktop/UH Research/Machine Learning/workflow2000.csvML.csv'
        contactFile = 'C:/Users/illum/Desktop/Protein graph comparisons/sample2000/Edgesloop4.holoCaM.run99.water2.pdb.csv'
        graphs = contactMapToDict(contactFile)
        features,labels = featureMatrices(featureFile)
        featureList = []
        adjacencies = []
        for frame in graphs.values():
            adjacencies.append(dictToGraph(frame))
        for feature in features.values():
            featureList.append(feature)
        # Create the directory
        os.mkdir(self.path)


        filename = os.path.join(self.path, f'graphs776')
        np.savez(filename, adjacencies = adjacencies, features = featureList, labels = labels)
    
    def read(self):
        output = []
        data = np.load(os.path.join(self.path, f'graphs776.npz'),allow_pickle=True)
        for frame in range(len(data['adjacencies'])):
            output.append(Graph(a=data['adjacencies'][frame],x=data['features'][frame],y=data['labels'][frame]))
        return output

class singleData(Dataset):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def read(self):
        return [self.graph]

dataset = data2000()

epochs = 250
batch_size = 50
learning_rate = 0.01
# Train/test split
np.random.seed(42)
np.random.shuffle(dataset)
split = int(0.8 * len(dataset))
data_tr, data_te = dataset[:split], dataset[split:]

from tensorflow.keras.losses import CategoricalCrossentropy
from spektral.data.loaders import DisjointLoader
from tensorflow.keras.metrics import CategoricalAccuracy

loader_tr = DisjointLoader(data_tr,batch_size=batch_size,epochs=epochs)
loader_te = DisjointLoader(data_te,batch_size=batch_size)



from spektral.models.general_gnn import GeneralGNN
from spektral.models.gcn import GCN
model = GeneralGNN(dataset.n_labels,activation="softmax")
#model = GCN(n_labels = dataset.n_labels,n_input_channels = dataset.n_node_features)
optimizer = tf.optimizers.Adam(learning_rate)
loss_fn = CategoricalCrossentropy()
acc_fn = CategoricalAccuracy()

# Training function
@tf.function(input_signature=loader_tr.tf_signature(), experimental_relax_shapes=True)
def train_on_batch(inputs, target):
    with tf.GradientTape() as tape:
        predictions = model(inputs, training=True)
        loss = loss_fn(target, predictions) + sum(model.losses)
        acc = acc_fn(target, predictions)

    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss, acc


# Evaluation function
def evaluate(loader):
    step = 0
    results = []
    for batch in loader:
        step += 1
        inputs, target = batch
        predictions = model(inputs, training=False)
        loss = loss_fn(target, predictions)
        predictionIndex = np.argmax(predictions,axis=0)
        trueIndex = np.argmax(target,axis=0)
        acc = acc_fn(target, predictions)
        results.append((loss, acc, len(target)))  # Keep track of batch size
        if step == loader.steps_per_epoch:
            results = np.array(results)
            return np.average(results[:, :-1], 0, weights=results[:, -1])


# Training loop
epoch = step = 0
results = []
for batch in loader_tr:
    step += 1
    loss, acc = train_on_batch(*batch)
    results.append((loss, acc))
    if step == loader_tr.steps_per_epoch:
        step = 0
        epoch += 1
        results_te = evaluate(loader_te)
        print(
            "Epoch {} - Train loss: {:.3f} - Train acc: {:.3f} - "
            "Test loss: {:.3f} - Test acc: {:.3f}".format(
                epoch, *np.mean(results, 0), *results_te
            )
        )

results_te = evaluate(loader_te)
print("Final results - Loss: {:.3f} - Acc: {:.3f}".format(*results_te))

from plotKerasResults import *
makeFigures(loader_te,model)

