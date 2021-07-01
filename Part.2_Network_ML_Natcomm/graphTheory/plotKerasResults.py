import matplotlib.pyplot as plt
import numpy as np
def makeFigures(loader,model):
    step = 0
    for batch in loader:
        step += 1
        inputs,target = batch
        predictions = model(inputs, training=False)
        pred = classesToCharges(predictions.numpy())
        y_test = oneHotsToCharges(target)
        true = np.asarray(y_test)
        mean = true.mean()
        sumSquares = np.power(true - mean,2).sum()
        sumResid = np.power(true-pred,2).sum()
        r2 = 1 - sumResid/sumSquares
        print('r-squared:',r2)
        rootMSE = ((np.power(true-pred,2).sum())/len(pred))**0.5
        print('rms:',rootMSE) 
        acc = accuracy(predictions,target)
        print('acc:',acc) 
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim(0, len(y_test))
        ax.set_ylim(0, 3)
        plt.plot(y_test, color='red', label = 'QM charge')
        plt.plot(pred, color='blue', label = 'Predicted charge')
        plt.legend(loc='best')
        plt.show()

def oneHotsToCharges(numpyArrays):
    minCharge = 1.1823
    charges = []
    chargeBins = []
    for n in range(np.shape(numpyArrays)[1]):
        chargeBins.append(minCharge + 0.01*n)
    chargeBins = np.asarray(chargeBins)
    for encoding in numpyArrays:
        charge = np.dot(encoding,chargeBins)
        charges.append(charge)
    return charges

def classesToCharges(numpyArrays):
    minCharge = 1.1823
    charges = []
    chargeBins = []
    for n in range(np.shape(numpyArrays)[1]):
        chargeBins.append(minCharge + 0.01*n)
    chargeBins = np.asarray(chargeBins)
    for encoding in numpyArrays:
        index = np.argmax(encoding)
        charge = chargeBins[index]
        charges.append(charge)
    return charges

def accuracy(pred,test):
    success = 0
    print(pred)
    print(test)
    for k in range(len(pred)):
        encoding = pred[k]
        index = np.argmax(encoding)
        print(index,np.argmax(test[k]))
        if index == np.argmax(test[k]):
            print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
            success+=1
    return success/len(pred)