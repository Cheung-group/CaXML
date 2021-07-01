import pandas as pd
import numpy as np
fileName = "workflow2000.csv"
path = r"C:\Users\illum\Desktop\UH Research\Machine Learning\%s" %fileName
data = pd.read_csv(path)
def longToWide(data):
    rows = data['componentnumber']
    numFrames = np.max(rows) + 1
    featureArray = {}
    features = ['Degree','Weighted Degree',
        'Eccentricity','closnesscentrality','harmonicclosnesscentrality',
        'betweenesscentrality','clustering','triangles']
    for i in range(14):
        for feature in features:
            featureArray["%s" %(i+1) + "%s" %feature] = [0] * numFrames
    for row in range(len(rows)):
        frame = rows[row]
        resNum = data.iloc[row]['Label'][-3:]
        resNum = analogous(int(resNum))
        for feature in features:
            featureArray["%s" %resNum + "%s" %feature][frame] = data.iloc[row][feature]
    machineLearningData = pd.DataFrame.from_dict(featureArray)
    machineLearningData.to_csv(path+"ML.csv")

def analogous(n):
    translation = {}
    for num in [20,56,93,129]:
        for k in range(12):
            translation[num + k] = k + 1
    if n in [13,14,15,16]:
        return n
    return translation[n]

longToWide(data)    




